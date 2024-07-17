from typing import OrderedDict
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound

from backend.settings import RedisDatabases
from tep_user.services import IPControlService

from .models import (Category, Color, Filter, FilterField, Material, Product,
                     ProductVariant, ProductVariantImage, ProductVariantInfo,
                     Size)
from rest_framework.status import HTTP_400_BAD_REQUEST


class FilterFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterField
        fields = '__all__'


class FilterSerializer(serializers.ModelSerializer):
    filter_field = FilterFieldSerializer(many=True)

    class Meta:
        model = Filter
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    filter = FilterSerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class ProductVariantInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantInfo
        fields = '__all__'


class ProductVariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantImage
        fields = '__all__'


class ProductVariantSerializer(serializers.ModelSerializer):
    sizes = SizeSerializer(many=True)
    colors = ColorSerializer(many=True)
    materials = MaterialSerializer(many=True)
    filter_field = FilterFieldSerializer(many=True)
    variant_info = ProductVariantInfoSerializer(read_only=True)
    variant_images = ProductVariantImageSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    product_variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class IncreaseNumberOfViewsSerializer(serializers.Serializer):
    """Serializer to increase product number of views."""
    id = serializers.IntegerField(required=True)

    class Meta:
        fields = ['id']

    def create(self, validated_data: OrderedDict) -> OrderedDict:
        """
        Override create method to increase number of views and check ip address.

        :param validated_data: validated data.

        :raises NotFound: raise http 404 error if product does not exists.
        :raises ValidationError: raise http 400 error if user try to increase number of views more that one time in week.

        :return: validated data.
        """
        try:
            instance = Product.objects.get(id=validated_data.get('id'))
        except Product.DoesNotExist:
            raise NotFound()
        
        ip_control_service = IPControlService(request=self.context.get('request'),  database=RedisDatabases.IP_CONTROL)

        if not ip_control_service.check_product_view_ip_access(instance.slug):
            raise ValidationError(code=HTTP_400_BAD_REQUEST)

        instance.number_of_views +=1
        
        return validated_data
