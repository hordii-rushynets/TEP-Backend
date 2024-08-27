from typing import Any

from django.db.models.query import QuerySet
from backend.settings import RedisDatabases

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request

from .models import Cart, CartItem
from .serializers import CartItemSerializer

from tep_user.services import IPControlService
from tep_user.authentication import IgnoreInvalidTokenAuthentication


class CartItemViewSet(viewsets.ModelViewSet):
    """CartItem ViewSet"""
    queryset = CartItem.objects.all()
    authentication_classes = [IgnoreInvalidTokenAuthentication]
    permission_classes = [AllowAny]
    serializer_class = CartItemSerializer
    pagination_class = None
    lookup_field = 'id'

    def _get_cart(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(tep_user=request.user)
        else:
            ip_service = IPControlService(request, RedisDatabases.IP_CONTROL)
            ip_address = ip_service.get_ip()
            cart, created = Cart.objects.get_or_create(ip_address=ip_address)
        return cart

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Create or update a CartItem for the user's cart.
        If the cart does not exist, it will be created.
        """
        cart = self._get_cart(request)

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
        cart = self._get_cart(self.request)
        return CartItem.objects.filter(cart=cart)

