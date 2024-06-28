from rest_framework import viewsets
from .models import CustomUser
from .serializers import CustomUserSerializer, RegisterSerializer, LoginSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from django.contrib.auth import authenticate


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
            user = serializer.save()
            if user:
                password = request.data.get('password')
                user.set_password(password)
                user.save()

                refresh = RefreshToken.for_user(user)
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }

                return Response({
                    'message': 'User registered successfully',
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
                'message': 'User logged in successfully',
                'token': token,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

