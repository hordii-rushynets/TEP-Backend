from django.urls import path
from .views import (
    UserRegistrationAPIView,
    OTPVerificationAPIView,
    PasswordResetRequestAPIView,
    PasswordResetConfirmAPIView,
    UserDeleteAPIView,
    UserProfileUpdateAPIView,
    UserLoginAPIView,
)


urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('verify-otp/', OTPVerificationAPIView.as_view(), name='verify-otp'),
    path('password/reset/', PasswordResetRequestAPIView.as_view(), name='password-reset-request'),
    path('password/reset/confirm/', PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),
    path('delete/', UserDeleteAPIView.as_view(), name='user-delete'),
    path('profile/update/', UserProfileUpdateAPIView.as_view(), name='user-profile-update'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
]
