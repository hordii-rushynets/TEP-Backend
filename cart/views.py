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
        Create or update a CartItem for the authenticated user's cart.
        If the cart does not exist, it will be created.
        """
        user = request.user
        cart, created = Cart.objects.get_or_create(tep_user=user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        product_variant = validated_data.get('product_variants')
        color = validated_data.get('color')
        material = validated_data.get('material')
        size = validated_data.get('size')
        filter_fields = validated_data.get('filter_field', [])
        quantity = validated_data.get('quantity', 1)

        existing_items = CartItem.objects.filter(
            cart=cart,
            product_variants=product_variant,
            color=color,
            material=material,
            size=size
        ).prefetch_related('filter_field')

        cart_item = None
        for item in existing_items:
            existing_filter_fields = set(item.filter_field.all())
            incoming_filter_fields = set(filter_fields)

            if existing_filter_fields == incoming_filter_fields:
                cart_item = item
                break

        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
            serializer = self.get_serializer(cart_item)
            return Response({
                'message': 'Item already exists in the cart. Quantity updated.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        cart_item = CartItem.objects.create(
            cart=cart,
            product_variants=product_variant,
            color=color,
            material=material,
            size=size,
            quantity=quantity
        )
        cart_item.filter_field.set(filter_fields)
        cart_item.save()
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self) -> QuerySet:
        """Get the queryset of CartItems for the authenticated user."""
        user = self.request.user
        return CartItem.objects.filter(cart__tep_user=user)
