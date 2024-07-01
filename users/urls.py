from django.urls import path
from .views import (
    UserRegistrationAPIView, OTPVerificationAPIView,
    PasswordResetRequestAPIView, PasswordResetConfirmAPIView,
    UserDeleteAPIView, UserProfileUpdateAPIView,
    UserLoginAPIView, NewOTPPasswordAPIView,
    GetUserDataViewSet, RefreshTokenView,
    AccessTokenVerifyView, RefreshTokenVerifyView
)


urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('register/verify-otp/', OTPVerificationAPIView.as_view(), name='verify-otp'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),

    path('password/reset/', PasswordResetRequestAPIView.as_view(), name='password-reset-request'),
    path('password/reset/confirm/', PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),

    path('profile/delete/', UserDeleteAPIView.as_view(), name='user-delete'),
    path('profile/update/', UserProfileUpdateAPIView.as_view(), name='user-profile-update'),
    path('profile/get/', GetUserDataViewSet.as_view(), name='profile-get'),

    path('new_otp/', NewOTPPasswordAPIView.as_view(), name='new-otp'),

    path('token/refresh/', RefreshTokenView.as_view(), name='refresh-token'),
    path('token/verify/access/', AccessTokenVerifyView.as_view(), name='token_verify_access'),
    path('token/verify/refresh/', RefreshTokenVerifyView.as_view(), name='token_verify_refresh'),

]
