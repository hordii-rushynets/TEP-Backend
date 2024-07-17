from rest_framework import serializers
from .models import Cart, CartItem
from tep_user.serializers import UserProfileSerializer
from store.models import ProductVariant, Color, Material, Size, FilterField


class CartItemSerializer(serializers.ModelSerializer):
    """CartItem Serializer"""
    product_variants = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all())
    color = serializers.PrimaryKeyRelatedField(queryset=Color.objects.all())
    material = serializers.PrimaryKeyRelatedField(queryset=Material.objects.all())
    size = serializers.PrimaryKeyRelatedField(queryset=Size.objects.all())
    filter_field = serializers.PrimaryKeyRelatedField(queryset=FilterField.objects.all())
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all(), required=False)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product_variants', 'color', 'material', 'size', 'filter_field', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    """Cart Serializer"""
    tep_user = UserProfileSerializer(read_only=True)
    order = CartItemSerializer(read_only=True, many=True)

    class Meta:
        model = Cart
        fields = ['tep_user', 'order']
