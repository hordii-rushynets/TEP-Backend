from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import (CustomUserSerializer, UserRegistrationSerializer,
                          OTPVerificationSerializer)
import secrets
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.conf import settings
from rest_framework_simplejwt.views import TokenVerifyView



class UserRegistrationAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            policy = serializer.validated_data['policy']
            wantInfo = serializer.validated_data['wantInfo']
            wholesale = serializer.validated_data['wholesale']

            if CustomUser.objects.filter(email=email).exists():
                return Response({'error': 'User with this email already exists.'},
                                status=status.HTTP_409_CONFLICT)

            user = CustomUser(
                email=email,
                first_name=first_name,
                last_name=last_name,
                policy=policy,
                wantInfo=wantInfo,
                wholesale=wholesale
            )
            user.set_password(password)
            otp = secrets.token_hex(3)
            user.otp = otp
            user.is_active = False
            user.save()
            print(otp)
            # send_otp_email(email, otp)

            return Response({'message': 'User registered. Please verify OTP sent to your email.'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


def send_otp_email(email, otp):
    send_mail(
        'OTP for Registration',
        f'Your OTP for registration is: {otp}',
        str(settings.EMAIL_HOST_USER),
        [email],
        fail_silently=False,
    )


class PasswordResetRequestAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')

        user = get_object_or_404(CustomUser, email=email)

        otp = secrets.token_hex(3)
        #send_otp_email(email, otp)
        print(otp)

        user.otp = otp
        user.save()

        return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)


class PasswordResetConfirmAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):

        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')

        user = get_object_or_404(CustomUser, email=email, otp=otp)

        user.set_password(new_password)
        user.otp = ''
        user.save()

        return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)


class UserDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({'message': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class UserProfileUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        token = request.headers.get('Authorization').split(' ')[1]

        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = CustomUser.objects.get(pk=user_id)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data

        serializer = CustomUserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            token = {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }
            return Response(token, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class OTPVerificationAPIView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']

            try:
                user = CustomUser.objects.get(email=email, otp=otp)
                user.is_active = True
                user.otp = ''
                user.save()

                refresh = RefreshToken.for_user(user)
                token = {
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                }

                return Response(token, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({'error': 'Invalid OTP or email'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewOTPPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = CustomUser.objects.get(email=email)

        otp = secrets.token_hex(3)
        user.otp = otp
        user.save()

        #send_otp_email(email, otp)
        print(otp)

        if user:
            return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GetUserDataViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        token = request.headers.get('Authorization').split(' ')[1]
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = CustomUser.objects.get(pk=user_id)
            serializer = CustomUserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

            refresh_token_obj = RefreshToken(refresh_token)
            access_token = str(refresh_token_obj.access_token)

            return Response({'access_token': access_token}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AccessTokenVerifyView(TokenVerifyView):
    pass


class RefreshTokenVerifyView(TokenVerifyView):
    pass



