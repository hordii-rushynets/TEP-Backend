from typing import OrderedDict

from rest_framework import serializers
from rest_framework.exceptions import NotFound, PermissionDenied

from backend.settings import RedisDatabases
from tep_user.services import IPControlService

from .models import (Category, Color, DimensionalGridSize, DimensionalGrid, Filter, FilterField, Material, Product,
                     ProductVariant, ProductVariantImage, ProductVariantInfo,
                     Size, FavoriteProduct)


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


class DimensionalGridSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimensionalGridSize
        fields = ['title_uk', 'title_en', 'title_ru', 'size_uk', 'size_en', 'size_ru']


class DimensionalGridSerializer(serializers.ModelSerializer):
    sizes = DimensionalGridSizeSerializer(read_only=True, many=True)

    class Meta:
        model = DimensionalGrid
        fields = ['id', 'title_uk', 'title_en', 'title_ru', 'sizes']


class ProductVariantSerializer(serializers.ModelSerializer):
    sizes = SizeSerializer(many=True)
    colors = ColorSerializer(many=True)
    materials = MaterialSerializer(many=True)
    filter_field = FilterFieldSerializer(many=True)
    variant_info = ProductVariantInfoSerializer(read_only=True)
    variant_images = ProductVariantImageSerializer(many=True, read_only=True)
    number_of_add_to_cart = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProductVariant
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    product_variants = ProductVariantSerializer(many=True, read_only=True)
    dimensional_grid = DimensionalGridSerializer(many=True, read_only=True)
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_is_favorite(self, product: Product) -> bool:
        """Get is_favorite flag for specific product."""
        request = self.context.get('request')

        try:
            if not request.user.is_authenticated:
                return False

            return FavoriteProduct.objects.get(user=request.user, product=product).favorite
        except FavoriteProduct.DoesNotExist:
            return False


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
        :raises PermissionDenied: raise http 403 error if user try to increase number of views more that one time in week.

        :return: validated data.
        """
        try:
            instance = Product.objects.get(id=validated_data.get('id'))
        except Product.DoesNotExist:
            raise NotFound()
        
        ip_control_service = IPControlService(request=self.context.get('request'),  database=RedisDatabases.IP_CONTROL)

        if not ip_control_service.check_product_number_of_views_ip_access(instance.slug):
            raise PermissionDenied()

        instance.number_of_views +=1
        instance.save()
        
        return validated_data


class SetFavoriteProductSerializer(serializers.Serializer):
    """Serializer to mark product as favorite by user."""
    id = serializers.IntegerField(required=True)
    favorite = serializers.BooleanField(required=True)

    class Meta:
        fields = ['id', 'favorite']

    def create(self, validated_data: OrderedDict) -> OrderedDict:
        """
        Override create method to favorite product.

        :param validated_data: validated data.

        :raises NotFound: raise http 404 error if product does not exists.
        :raises PermissionDenied: raise http 403 error if user try to mark product as favorite more that 6 times in minute.

        :return: validated data.
        """
        try:
            instance = Product.objects.get(id=validated_data.get('id'))
        except FavoriteProduct.DoesNotExist:
            raise NotFound()

        ip_control_service = IPControlService(request=self.context.get('request'),  database=RedisDatabases.IP_CONTROL)

        if not ip_control_service.check_product_set_favorite_ip_access(instance.slug):
            raise PermissionDenied()
        
        favorite = self.validated_data.get('favorite')
        request = self.context.get('request')

        FavoriteProduct.objects.update_or_create(
            product=instance,
            user=request.user,
            defaults={'favorite': favorite}
        )

        return validated_data
