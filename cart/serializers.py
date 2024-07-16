from rest_framework import serializers
from .models import Cart, CartItem
from tep_user.serializers import UserProfileSerializer
from store.serializers import (MaterialSerializer, SizeSerializer, FilterFieldSerializer, ColorSerializer,
                               ProductVariantSerializer)


class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for CartItem model.

    Fields:
    - cart: The cart to which the item belongs.
    - product_variants: Serialized representation of the product variants in the cart item.
    - color: Serialized representation of the color of the product.
    - material: Serialized representation of the material of the product.
    - size: Serialized representation of the size of the product.
    - filter_field: Serialized representation of additional filter fields associated with the product.
    - quantity: The quantity of the product in the cart.
    """

    product_variants = ProductVariantSerializer(read_only=True)
    color = ColorSerializer(read_only=True)
    material = MaterialSerializer(read_only=True)
    size = SizeSerializer(read_only=True)
    filter_field = FilterFieldSerializer(many=True, read_only=True)

    class Meta:
        model = CartItem
        fields = ['cart', 'product_variants', 'color', 'material', 'size', 'filter_field', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for Cart model.

    Fields:
    - tep_user: Serialized representation of the user profile associated with the cart.
    - order: Serialized representation of the cart items (many items).
    """

    tep_user = UserProfileSerializer(read_only=True)
    order = CartItemSerializer(read_only=True, many=True)

    class Meta:
        model = Cart
        fields = ['tep_user', 'order']
