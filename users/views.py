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
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            if CustomUser.objects.filter(email=email).exists():
                return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            user = CustomUser(email=email)
            user.set_password(password)
            user.save()

            otp = secrets.token_hex(3)
            user.otp = otp
            user.save()
            #send_otp_email(email, otp)
            print(otp)

            return Response({'message': 'User registered. Please verify OTP sent to your email.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Function to send OTP via email
def send_otp_email(email, otp):
    send_mail(
        'OTP for Registration',
        f'Your OTP for registration is: {otp}',
        'from@example.com',
        [email],
        fail_silently=False,
    )


class PasswordResetRequestAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')

        user = get_object_or_404(CustomUser, email=email)

        otp = secrets.token_hex(3)
        send_otp_email(email, otp)

        # Save OTP to user's record or another appropriate store

        return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)


class PasswordResetConfirmAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')

        user = get_object_or_404(CustomUser, email=email)

        # Set new password
        user.set_password(new_password)
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
        user = request.user
        data = request.data

        # Validate OTP (check against the stored OTP or other logic)
        otp = data.get('otp')
        # Implement your OTP validation logic here

        # Update user profile data
        serializer = CustomUserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user:
            # Generate JWT tokens
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
                token = {'token': str(refresh.access_token)}

                return Response(token, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({'error': 'Invalid OTP or email'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)