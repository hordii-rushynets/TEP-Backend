from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Order, OrderItem
from .services.factory import get_delivery_service

from store.serializers import (ProductVariantSerializer,
                               MaterialSerializer,
                               ColorSerializer,
                               SizeSerializer)


class OrderItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)
    color = ColorSerializer(read_only=True)
    material = MaterialSerializer(read_only=True)
    size = SizeSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_variant', 'color', 'material', 'size', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True, read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'number', 'post_type', 'order_item', 'status', 'created_at']

    def get_status(self, obj):
        try:
            delivery_service = get_delivery_service(obj.post_type)
            status_list = delivery_service.track_parcel(obj.number)

            if status_list:
                return status_list[-1]
            return None
        except ValidationError:
            return None
