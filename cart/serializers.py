from rest_framework import serializers
from .models import Cart, CartItem
from tep_user.serializers import UserProfileSerializer
from store.models import ProductVariant, Color, Material, Size, FilterField
from store.serializers import (ProductVariantSerializer,
                               ColorSerializer,
                               MaterialSerializer,
                               SizeSerializer,
                               FilterFieldSerializer)


class CartItemSerializer(serializers.ModelSerializer):
    """CartItem Serializer"""
    product_variants = ProductVariantSerializer(read_only=True)
    product_variants_id = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all(), write_only=True,
                                                             source='product_variants')

    color = ColorSerializer(read_only=True)
    color_id = serializers.PrimaryKeyRelatedField(queryset=Color.objects.all(), write_only=True, source='color',
                                                  required=False)

    material = MaterialSerializer(read_only=True)
    material_id = serializers.PrimaryKeyRelatedField(queryset=Material.objects.all(), write_only=True,
                                                     source='material', required=False)

    size = SizeSerializer(read_only=True)
    size_id = serializers.PrimaryKeyRelatedField(queryset=Size.objects.all(), write_only=True, source='size', required=False)

    filter_field = FilterFieldSerializer(read_only=True, many=True)
    filter_field_ids = serializers.PrimaryKeyRelatedField(queryset=FilterField.objects.all(), many=True,
                                                          write_only=True, source='filter_field', required=False)

    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all(), required=False)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product_variants', 'product_variants_id', 'color', 'color_id', 'material',
                  'material_id', 'size', 'size_id', 'filter_field', 'filter_field_ids', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    """Cart Serializer"""
    tep_user = UserProfileSerializer(read_only=True)
    order = CartItemSerializer(read_only=True, many=True)

    class Meta:
        model = Cart
        fields = ['tep_user', 'order']
