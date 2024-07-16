from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Cart, Order
from .serializers import CartSerializer, OrderSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    lookup_field = 'id'


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    lookup_field = 'id'
