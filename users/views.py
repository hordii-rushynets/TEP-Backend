from rest_framework import viewsets
from .models import CustomUser
from .serializers import CustomUserSerializer, RegisterSerializer, LoginSerializer
from rest_framework import permissions
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.utils.crypto import get_random_string


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'


class RegisterView(APIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Generate one-time password
            otp = get_random_string(length=6, allowed_chars='0123456789')

            # Do not save user yet, wait for email confirmation
            user = serializer.save(is_active=False, otp=otp)

            # Send email with one-time password
            subject = 'Email confirmation'
            message = f'Your one-time confirmation password: {otp}'
            from_email = settings.EMAIL_HOST_USER
            to_email = user.email
            send_mail(subject, message, from_email, [to_email])

            if user:
                refresh = RefreshToken.for_user(user)
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response({
                    'token': token,
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        user = authenticate(request, username=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response({
                'token': token,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

