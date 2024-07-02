from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email', 'policy', 'wantInfo', 'wholesale', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password', 'policy', 'wantInfo', 'wholesale', 'is_active')
        extra_kwargs = {'password': {'write_only': True}}


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
