from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.response import Response
from typing import Tuple, Any
from rest_framework.request import Request
from django.db.models.query import QuerySet


class CartViewSet(viewsets.ModelViewSet):
    """Cart ViewSet"""
    queryset = Cart.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        return Cart.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)

        if created:
            serializer = self.get_serializer(cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Cart already exists for this user."}, status=status.HTTP_400_BAD_REQUEST)


class CartItemViewSet(viewsets.ModelViewSet):
    """CartItem ViewSet"""
    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer
    lookup_field = 'id'

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
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self) -> QuerySet:
        """Get the queryset of CartItems for the authenticated user."""
        user = self.request.user
        return CartItem.objects.filter(cart__tep_user=user)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        List all CartItems for the authenticated user.
        If no CartItems exist, create an empty cart for the user.
        """
        queryset = self.get_queryset()
        if not queryset.exists():
            Cart.objects.get_or_create(tep_user=request.user)
            return Response({"detail": "Cart was created for the user, but there are no items."},
                            status=status.HTTP_201_CREATED)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
