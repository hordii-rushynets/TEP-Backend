from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from store.serializers import ProductVariantSerializer
from .models import Order
from .services.factory import  get_delivery_service


class OrderSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(many=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'number', 'post_type', 'product_variant', 'status']

    def get_status(self, obj):
        try:
            delivery_service = get_delivery_service(obj.post_type)
            status_list = delivery_service.track_parcel(obj.number)

            if status_list:
                return status_list[-1]
            return None
        except ValidationError:
            return None
