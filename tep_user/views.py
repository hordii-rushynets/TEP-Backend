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
from tep_user.serializers import (UserConfirmCodeSerializer,
                                  UserForgetPasswordSerializer,
                                  ForgetPasswordConfirmCodeSerializer,
                                  UserLoginSerializer, UserProfileSerializer,
                                  UserRegistrationSerializer,
                                  UserResentCodeSerializer,
                                  UserEmailUpdateRequestSerializer,
                                  UserEmailUpdateConfirmSerializer,
                                  UserPasswordUpdateRequestSerializer,
                                  UserAddressSerializer)

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework_simplejwt.tokens import RefreshToken
from social_django.utils import psa


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


class UserAddressView(generics.RetrieveUpdateDestroyAPIView):
    """User address view."""
    serializer_class = UserAddressSerializer
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


class GoogleLoginAPIView(APIView):
    def get(self, request, *args, **kwargs):
        redirect_uri = request.build_absolute_uri('/auth/complete/google/')
        return redirect(
            f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY}&redirect_uri={redirect_uri}&scope=email profile"
        )


class GoogleCallbackAPIView(APIView):
    @psa('social:complete')
    def get(self, request, *args, **kwargs):
        backend = request.backend
        user = request.backend.do_auth(request.GET.get('code'))
        if user:
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return JsonResponse({'error': 'Authentication failed'}, status=status.HTTP_400_BAD_REQUEST)


