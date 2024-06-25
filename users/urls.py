from django.urls import path
from .views import UserRegisterViewSet, ObtainTokenViewSet, UserViewSet

urlpatterns = [
    path('register/', UserRegisterViewSet.as_view(), name='register'),
    path('token/', ObtainTokenViewSet.as_view(), name='token_obtain'),

    path('get/', UserViewSet.as_view({'get': 'list'})),
    path('get/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}))
]
