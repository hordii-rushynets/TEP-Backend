from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.response import Response
from typing import Tuple, Any
from rest_framework.request import Request
from django.db.models.query import QuerySet


class CartItemViewSet(viewsets.ModelViewSet):
    """CartItem ViewSet"""
    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer
    pagination_class = None
    lookup_field = 'id'

    def get_object(self):
        return super().get_object()

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Create a new CartItem for the authenticated user's cart.
        If the cart does not exist, it will be created.
        """
        user = request.user
        cart, created = Cart.objects.get_or_create(tep_user=user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(cart=cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self) -> QuerySet:
        """Get the queryset of CartItems for the authenticated user."""
        user = self.request.user
        return CartItem.objects.filter(cart__tep_user=user)
