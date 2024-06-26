from django.urls import path
from .views import CustomUserViewSet

urlpatterns = [
    path('register/', CustomUserViewSet.as_view({'get': 'list', 'post': 'create'}), name='register'),

    path('<int:pk>/', CustomUserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

]