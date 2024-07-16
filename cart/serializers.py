from rest_framework import serializers
from .models import Cart, CartItem
from tep_user.serializers import UserProfileSerializer
from store.serializers import (MaterialSerializer, SizeSerializer, FilterFieldSerializer, ColorSerializer,
                               ProductVariantSerializer)


class CartItemSerializer(serializers.ModelSerializer):
    product_variants = ProductVariantSerializer(read_only=True)
    color = ColorSerializer(read_only=True)
    material = MaterialSerializer(read_only=True)
    size = SizeSerializer(read_only=True)
    filter_field = FilterFieldSerializer(many=True, read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    tep_user = UserProfileSerializer(read_only=True)
    order = CartItemSerializer(read_only=True, many=True)

    class Meta:
        model = Cart
        fields = '__all__'
