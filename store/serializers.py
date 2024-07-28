from typing import OrderedDict

from rest_framework import serializers
from rest_framework.exceptions import NotFound, PermissionDenied

from backend.settings import RedisDatabases
from tep_user.services import IPControlService

from .models import (Category, Color, DimensionalGridSize, DimensionalGrid, Filter, FilterField, Material, Product,
                     ProductVariant, ProductVariantImage, ProductVariantInfo, InspirationImage,
                     Size, FavoriteProduct, Feedback, FeedbackImage, FeedbackVote, ProductImage)

from tep_user.serializers import UserProfileSerializer

from cart.models import CartItem, Cart




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
        fields = ['title_uk', 'title_en', 'size_uk', 'size_en']


class DimensionalGridSerializer(serializers.ModelSerializer):
    sizes = DimensionalGridSizeSerializer(read_only=True, many=True)

    class Meta:
        model = DimensionalGrid
        fields = ['id', 'title_uk', 'title_en', 'sizes']


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


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    product_variants = ProductVariantSerializer(many=True, read_only=True)
    dimensional_grid = DimensionalGridSerializer(many=True, read_only=True)
    is_favorite = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    image_list = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True, required=False
    )
    svg_image = serializers.FileField()
    in_cart = serializers.SerializerMethodField()

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

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_in_cart(self, product: Product) -> bool:
        """Check if the product is in the cart for the current user."""
        request = self.context.get('request')

        if not request.user.is_authenticated:
            return False

        try:
            cart = Cart.objects.get(tep_user=request.user)
            return CartItem.objects.filter(
                cart=cart,
                product_variants__product=product
            ).exists()
        except Cart.DoesNotExist:
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


class FeedbackVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackVote
        fields = ['id', 'tep_user', 'feedback', 'is_like']


class FeedbackImageSerializer(serializers.ModelSerializer):
    """Feedback Image Serializer"""
    class Meta:
        model = FeedbackImage
        fields = ['id', 'image']


class FeedbackSerializer(serializers.ModelSerializer):
    """Feedback Serializer"""
    tep_user = UserProfileSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')
    feedback_images = FeedbackImageSerializer(many=True, read_only=True)
    user_vote = serializers.SerializerMethodField()
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True, required=False
    )

    class Meta:
        model = Feedback
        fields = ['id', 'tep_user', 'product', 'product_id', 'text', 'like_number', 'dislike_number', 'evaluation',
                  'feedback_images', 'creation_time', 'user_vote', 'images']

    def get_user_vote(self, obj):
        user = self.context['request'].user
        return obj.get_user_vote(user)

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        feedback = super().create(validated_data)

        for image_data in images_data:
            FeedbackImage.objects.create(feedback=feedback, image=image_data)

        return feedback


class FullDataSerializer(serializers.Serializer):
    size = SizeSerializer(read_only=True, many=True)
    color = ColorSerializer(read_only=True, many=True)
    material = MaterialSerializer(read_only=True, many=True)

    class Meta:
        fields = ['size', 'color', 'material']


class InspirationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspirationImage
        fields = ['image']
