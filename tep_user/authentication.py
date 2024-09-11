"""Authentication backend for tep_user app."""
from typing import Union

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AbstractUser

from rest_framework.request import Request
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class EmailBackend(ModelBackend):
    """Backend to login via email."""
    def authenticate(self, request: Request, email: str=None, password: str=None, **kwargs) -> AbstractUser:
        """
        Override authenticate method to login via email.

        :param request: http request.
        :param email: email.
        :param password: password.

        :return: user.
        """
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

    def get_user(self, user_id: int) -> Union[AbstractUser, None]:
        """
        Get user.

        :param user_id: user id.

        :return: user.
        """
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


class IgnoreInvalidTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except AuthenticationFailed:
            return None
