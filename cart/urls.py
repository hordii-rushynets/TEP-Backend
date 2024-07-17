from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, CartItemViewSet

router = DefaultRouter()
router.register('', CartViewSet, basename='cart')
router.register('item', CartItemViewSet, basename='cart-item')


urlpatterns = [
    path('', include(router.urls)),
]