"""Views for tep_user app."""
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from tep_user.models import TEPUser
from tep_user.tasks import subscribe_to_mail_chimp
from tep_user.serializers import (UserConfirmCodeSerializer,
                                  UserForgetPasswordSerializer,
                                  ForgetPasswordConfirmCodeSerializer,
                                  UserLoginSerializer, UserProfileSerializer,
                                  UserRegistrationSerializer,
                                  UserResentCodeSerializer,
                                  UserEmailUpdateRequestSerializer,
                                  UserEmailUpdateConfirmSerializer,
                                  UserPasswordUpdateRequestSerializer
                                  )

from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests


class UserRegistrationViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """Registration viewset."""
    queryset = TEPUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    @action(methods=['post'], detail=False)
    def resent(self, request: Request) -> Response:
        serializer = UserResentCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    
    @action(methods=['post'], detail=False)
    def confirm(self, request: Request) -> Response:
        serializer = UserConfirmCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = TEPUser.objects.get(email=request.data.get('email'))
        if user.interested_in_wholesale or user.subscribed_to_updates:
            subscribe_to_mail_chimp.delay(user.email, user.first_name, user.last_name)

        return Response(status=status.HTTP_200_OK)


class UserLoginAPIView(TokenObtainPairView):
    """Login view."""
    serializer_class = UserLoginSerializer


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    """User profile view."""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ResetPasswordView(APIView):
    """Reset password view."""
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Set a new user password using the http POST method.

        :param request: http request.

        :return: http response.
        """
        serializer = UserPasswordUpdateRequestSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)


class ForgetPasswordViewSet(CreateModelMixin, viewsets.GenericViewSet):
    queryset = TEPUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserForgetPasswordSerializer
    
    @action(methods=['post'], detail=False)
    def confirm(self, request: Request) -> Response:
        serializer = ForgetPasswordConfirmCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class UserEmailUpdateViewSet(viewsets.GenericViewSet):
    """ViewSet to change the user's email."""
    queryset = TEPUser.objects.all()
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=False, url_path='request')
    def request_update_email(self, request):
        user = request.user
        serializer = UserEmailUpdateRequestSerializer(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='confirm')
    def confirm_update_email(self, request):
        user = request.user
        serializer = UserEmailUpdateConfirmSerializer(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get('token')

        try:
            id_info = id_token.verify_oauth2_token(token, requests.Request())

            if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            user, created = TEPUser.objects.get_or_create(
                email=id_info['email'],
                defaults={
                    'username': id_info['email'],
                    'first_name': id_info.get('given_name', ''),
                    'last_name': id_info.get('family_name', ''),
                }
            )

            refresh = RefreshToken.for_user(user)
            data = {
                'email': user.email,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
