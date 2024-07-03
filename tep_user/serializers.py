from typing import OrderedDict
from django.db import transaction, models
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from tep_user.services import IPControlService, EmailService
from tep_user import constants as user_const
from tep_user.models import TEPUser
from tep_user.services import UserService
from tep_user.utils import send_email_code
from backend.settings import RedisDatabases


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Registration serializer."""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = TEPUser
        fields = ['email', 'first_name', 'last_name', 'password', 'privacy_policy_accepted', 'interested_in_wholesale', 'subscribed_to_updates']

    @staticmethod
    def validate_email(email: str) -> str:
        """
        Validate email.

        :param email: user email.

        :raises ValidationError: User with current email already exists.

        :return: email.
        """

        if user := TEPUser.objects.filter(email=email).first():
            raise ValidationError(
                user.is_active and user_const.USER_ALREADY_EXISTS_ERROR or user_const.USER_NOT_ACTIVE_ERROR,
                code=HTTP_400_BAD_REQUEST
            )

        return email

    @transaction.atomic
    def create(self, validated_data: dict) -> TEPUser:
        """
        Create user.

        :param validated_data: validated data.

        :return: User model.
        """
        ip_control = IPControlService(request=self.context['request'], database=RedisDatabases.LOGIN_CODE)
        if not ip_control.check_registration_ip_access():
            raise ValidationError(detail=user_const.USER_REGISTER_IP_ERROR, code=status.HTTP_400_BAD_REQUEST)

        email = validated_data.pop('email')
        user = TEPUser.objects.create_user(
            email=email,
            username=email,
            is_active=False,
            **validated_data
        )

        send_email_code(email, user.full_name)
        return user


class UserResentCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs: dict) -> dict:
        attrs = super().validate(attrs)

        user_qs = TEPUser.objects.filter(email=attrs.get('email'), is_active=False)
        if not user_qs.exists():
            raise ValidationError(detail=user_const.CONFIRMATION_USER, code=status.HTTP_400_BAD_REQUEST)

        attrs['user'] = user_qs.first()
        return attrs

    @transaction.atomic
    def create(self, validated_data: dict) -> dict:
        user: TEPUser = validated_data.pop('user')
        email = validated_data['email']

        send_email_code(email, user.full_name)
        return validated_data


class UserConfirmCodeSerializer(serializers.Serializer):
    """Serializer to conifrm email code."""
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)

    def validate_code(self, code: str) -> str:
        """
        Check the verification code for the specified email.

        :param code: verification code.
        
        :raises ValidationError: if confirmation code does not exists or is not equal to code sent by user.

        :return: valid code.
        """
        data = self._kwargs.get('data')

        confirmation_code = UserService.get_code(email=data.get('email'))
        if not confirmation_code or str(code) != str(confirmation_code):
            raise ValidationError(detail=user_const.CONFIRMATION_WRONG_CODE, code=status.HTTP_400_BAD_REQUEST)
        return code

    def validate_email(self, email: str) -> str:
        """
        Check if a user with the current email exists.

        :param email: user email.

        :raises ValidationError: if a user with current email does not exists or is_active flag is equal to True for this user.

        :return: valid email.
        """
        user_qs = self.get_user_queryset(email)
        if not user_qs.exists():
            raise ValidationError(detail=user_const.CONFIRMATION_USER, code=status.HTTP_400_BAD_REQUEST)
        
        return email

    @staticmethod
    def get_user_queryset(email: str) -> models.QuerySet:
        """
        Get user queryset.
        
        :param email: request email.

        :return: queryset of users.
        """
        return TEPUser.objects.filter(email=email, is_active=False)

    def create(self, validated_data: dict) -> dict:
        TEPUser.objects.filter(email=validated_data.get('email')).update(is_active=True)
        return validated_data


class ForgetPasswordConfirmCodeSerializer(UserConfirmCodeSerializer):
    """Serializer to conifrm email code during forgot password."""
    @staticmethod
    def get_user_queryset(email: str) -> models.QuerySet:
        """
        Get user queryset.
        
        :param email: request email.

        :return: queryset of users.
        """
        return TEPUser.objects.filter(email=email, is_active=True)
    
    @transaction.atomic
    def create(self, validated_data: OrderedDict) -> OrderedDict:
        email = validated_data.get('email')
        user = self.get_user_queryset(email).first()

        if user:
            password = UserService.gen_password()
            user.set_password(password)
            user.save()

            EmailService(recipient=user.email, context={'full_name': user.full_name}).new_password(password).send()
        return validated_data

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer to get or update profile."""
    class Meta:
        model = TEPUser
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone_number', 'profile_picture', 'privacy_policy_accepted'
        ]


class UserLoginSerializer(TokenObtainPairSerializer):
    """Login serializer."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs: dict) -> dict:
        """
        Validate user credentials and generate token response.

        :param attrs: Tuple containing the user credentials (email and password).

        :return: Dictionary containing the token response data, including access and refresh tokens and user data.
        """
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)  # noqa
        return data


class UserResetPasswordSerializer(serializers.ModelSerializer):
    """Serializer to reset password."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = TEPUser
        fields = ['password']

    def save(self) -> None:
        """Save new user password."""
        self.instance.set_password(self.validated_data['password'])
        self.instance.save()


class UserForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs: dict) -> dict:
        attrs = super().validate(attrs)

        if not (user := TEPUser.objects.filter(email=attrs.get('email'), is_active=True).first()):
            raise ValidationError(detail=user_const.FORGET_PASSWORD, code=status.HTTP_400_BAD_REQUEST)

        self.instance = user
        send_email_code(user.email, user.full_name)
        return attrs
