from django.urls import path
from .views import CustomUserViewSet, RegisterView, LoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('<int:pk>/', CustomUserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

]