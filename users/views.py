from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomUserSerializer, UserRegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserRegisterViewSet(generics.CreateAPIView):
    """
    View for user registration.
    """
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]  # Allow any user (unauthenticated) to register

    def perform_create(self, serializer):
        user = serializer.save()  # Save the user
        refresh = RefreshToken.for_user(user)  # Generate JWT tokens
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class ObtainTokenViewSet(generics.GenericAPIView):
    """
    View to obtain JWT token.
    """
    serializer_class = CustomUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
