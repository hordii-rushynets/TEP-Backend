from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomUserSerializer, UserRegisterSerializer


class UserRegisterView(generics.CreateAPIView):
    """
    View for user registration.
    """
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]  # Allow any user (unauthenticated) to register


class ObtainTokenView(generics.GenericAPIView):
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
