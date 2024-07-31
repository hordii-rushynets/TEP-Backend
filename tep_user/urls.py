from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView

from .views import (
    ResetPasswordView,
    ProfileView,
    UserLoginAPIView,
    UserRegistrationViewSet,
    ForgetPasswordViewSet,
    UserEmailUpdateViewSet,
)

router = DefaultRouter()
router.register('register', UserRegistrationViewSet, basename='register')
router.register('password/forget', ForgetPasswordViewSet, basename='forget_password')
router.register('update/email', UserEmailUpdateViewSet, basename='update_email')

urlpatterns = router.urls + [
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path('password/reset/', ResetPasswordView.as_view(), name='reset_password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='update_profile'),
    path('address/', UserAddressView.as_view(), name='user_address'),
    path('auth/', include('allauth.urls')),
    path('auth/social/', include('allauth.socialaccount.urls')),
]
