from rest_framework import serializers
from .models import Category, Product, Size, Color, Material, ProductVariant, ProductVariantInfo


class CategorySerializer(serializers.ModelSerializer):
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


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'


class ProductVariantSerializer(serializers.ModelSerializer):
    sizes = SizeSerializer(many=True)
    colors = ColorSerializer(many=True)
    materials = MaterialSerializer(many=True)

    class Meta:
        model = ProductVariant
        fields = '__all__'


class ProductVariantInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantInfo
        fields = '__all__'
