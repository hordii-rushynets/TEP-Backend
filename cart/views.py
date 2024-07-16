from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartViewSet(viewsets.ModelViewSet):
    """Cart ViewSet"""
    queryset = Cart.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    lookup_field = 'id'


class CartItemViewSet(viewsets.ModelViewSet):
    """CartItem ViewSet"""
    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer
    lookup_field = 'id'
