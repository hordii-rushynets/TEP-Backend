from django.urls import path
from .views import UserRegisterView, ObtainTokenView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('token/', ObtainTokenView.as_view(), name='token_obtain'),
]
