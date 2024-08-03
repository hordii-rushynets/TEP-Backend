from rest_framework import serializers
from .models import OrderNumber


class OrderNumberSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderNumber
        fields = ['number', 'tep_user', 'post_type']

