from rest_framework import serializers
from .models import Order
from store.serializers import ProductVariantSerializer


class OrderSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'number', 'post_type', 'product_variant']
