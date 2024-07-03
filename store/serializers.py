from rest_framework import serializers
from .models import (Category, Product, Size, Color, Material, ProductVariant,
                     ProductVariantInfo, СustomFilterFields)


class СustomFilterFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = СustomFilterFields
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    filters = СustomFilterFieldsSerializer(many=True)

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
