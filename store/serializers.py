from rest_framework import serializers
from .models import (Category, Product, Size, Color, Material, ProductVariant,
                     ProductVariantInfo, Filter, FilterField)


class FilterFieldSerializer(serializers.ModelSerializer):
    class Meta:

        model = FilterField
        fields = '__all__'


class FilterSerializer(serializers.ModelSerializer):
    filter_fields = FilterFieldSerializer(many=True)

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


class ProductVariantSerializer(serializers.ModelSerializer):
    sizes = SizeSerializer(many=True)
    colors = ColorSerializer(many=True)
    materials = MaterialSerializer(many=True)
    filter_field = FilterFieldSerializer(many=True)

    class Meta:
        model = ProductVariant
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    product_variants = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        
    def get_product_variants(self, obj):
        variants = obj.productvariant_set.all()
        return ProductVariantSerializer(variants, many=True).data
      

class ProductVariantInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantInfo
        fields = '__all__'
