from rest_framework import serializers
from .models import Cart
from tep_user.serializers import UserProfileSerializer
from store.serializers import ProductVariantSerializer


class CartSerializer(serializers.ModelSerializer):
    tep_user = UserProfileSerializer()
    product_variants = ProductVariantSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('tep_user', 'product_variants')