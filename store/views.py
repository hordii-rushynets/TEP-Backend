from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.request import Request
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import QuerySet, Count
from django.shortcuts import get_object_or_404
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend

from transliterate import translit
from .tasks import import_data_task
from .models import (Category, Product, Size, Color, Material, ProductVariant,
                     ProductVariantInfo, Filter, FavoriteProduct, Feedback, FeedbackVote, InspirationImage)
from .serializers import (
    CategorySerializer, ProductSerializer, SizeSerializer,
    ColorSerializer, MaterialSerializer, ProductVariantSerializer,
    ProductVariantInfoSerializer, FilterSerializer, IncreaseNumberOfViewsSerializer,
    SetFavoriteProductSerializer, FeedbackSerializer, FullDataSerializer, InspirationImageSerializer,
    CategoryProductVariantSerializer
)
from .filters import ProductFilter, CategoryFilter, ProductVariantFilter, FeedbackFilter, CompareProductFilter

from cart.models import CartItem, Cart
from tep_user.authentication import IgnoreInvalidTokenAuthentication
from tep_user.services import IPControlService, RedisDatabases


def generate_latin_slug(string):
    latin_string = translit(string, 'uk', reversed=True)
    clean_string = ''.join(e for e in latin_string if e.isalnum() or e == ' ')
    slug = clean_string.replace(' ', '-').lower()
    return slug


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [IgnoreInvalidTokenAuthentication]
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CategoryFilter


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [IgnoreInvalidTokenAuthentication]
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ProductFilter
    ordering_fields = ['number_of_views', 'number_of_add_to_cart', 'last_modified']
    ordering = ['-number_of_views', '-number_of_add_to_cart']

    def get_queryset(self):
        """Counts how many times an item has been added to the cart."""
        return Product.objects.annotate(
            number_of_add_to_cart=Count('product_variants__cart_item')
        )

    @action(methods=['post'], detail=False)
    def increase_number_of_view(self, request: Request) -> Response:
        """
        Endpoint to increase product number of views.
        
        :param request: http request.

        :return: response
        """
        serializer = IncreaseNumberOfViewsSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class FavoriteProductViewset(CreateModelMixin, ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        serializers = {
            'create': SetFavoriteProductSerializer,
            'list': ProductSerializer
        }
        return serializers[self.action]

    def get_queryset(self) -> QuerySet:
        """Return products that marked as favorite."""
        product_ids = FavoriteProduct.objects.filter(favorite=True, user=self.request.user).values_list('product__id', flat=True)
        return Product.objects.filter(id__in=product_ids)

    def destroy(self, request, *args, **kwargs):
        """Remove all products from favorites."""
        num_deleted, _ = FavoriteProduct.objects.filter(user=request.user).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class SizeViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [IgnoreInvalidTokenAuthentication]
    permission_classes = [AllowAny]
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    lookup_field = 'slug'


class ColorViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [IgnoreInvalidTokenAuthentication]
    permission_classes = [AllowAny]
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    lookup_field = 'slug'


class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [IgnoreInvalidTokenAuthentication]
    permission_classes = [AllowAny]
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    lookup_field = 'slug'


class ProductVariantViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [IgnoreInvalidTokenAuthentication]
    permission_classes = [AllowAny]
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductVariantFilter


class ProductVariantInfoViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [IgnoreInvalidTokenAuthentication]
    permission_classes = [AllowAny]
    queryset = ProductVariantInfo.objects.all()
    serializer_class = ProductVariantInfoSerializer
    lookup_field = 'slug'


class FilterViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [IgnoreInvalidTokenAuthentication]
    permission_classes = [AllowAny]
    queryset = Filter.objects.all()
    serializer_class = FilterSerializer
    lookup_field = 'id'


class FeedbackViewSet(ListModelMixin,
                      CreateModelMixin,
                      RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """Feedback ViewSet"""
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    authentication_classes = [IgnoreInvalidTokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FeedbackFilter

    def create(self, request, *args, **kwargs):
        """Create a new object instance."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        feedback = serializer.save(tep_user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def like(self, request, *args, **kwargs):
        """Like functionality."""
        feedback = self.get_object()
        user = request.user
        vote, created = FeedbackVote.objects.get_or_create(tep_user=user, feedback=feedback)

        if vote.is_like == True:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if vote.is_like == False:
            vote.is_like = True
            vote.save()
            feedback.dislike_number -= 1
            feedback.like_number += 1
        elif created or vote.is_like is None:
            vote.is_like = True
            vote.save()
            feedback.like_number += 1

        feedback.save()

        return Response({
            'like_number': feedback.like_number,
            'dislike_number': feedback.dislike_number
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def dislike(self, request, *args, **kwargs):
        """Dislike functionality."""
        feedback = self.get_object()
        user = request.user
        vote, created = FeedbackVote.objects.get_or_create(tep_user=user, feedback=feedback)

        if vote.is_like == False:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if vote.is_like == True:
            vote.is_like = False
            vote.save()
            feedback.like_number -= 1
            feedback.dislike_number += 1
        elif created or vote.is_like is None:
            vote.is_like = False
            vote.save()
            feedback.dislike_number += 1

        feedback.save()

        return Response({
            'like_number': feedback.like_number,
            'dislike_number': feedback.dislike_number
        }, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


@method_decorator(csrf_exempt, name='dispatch')
class ProductsImport(APIView):
    def post(self, request):
        data = request.data
        # import_data_task(data)
        import_data_task.delay(data)
        return Response({'status': 'success'})


class FullDataViewSet(viewsets.ViewSet):
    authentication_classes = [IgnoreInvalidTokenAuthentication]
    permission_classes = [AllowAny]

    def list(self, request):
        size = Size.objects.all()
        color = Color.objects.all()
        material = Material.objects.all()

        data = {
            'size': size,
            'color': color,
            'material': material
        }

        serializer = FullDataSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompareProductViewSet(ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [IgnoreInvalidTokenAuthentication]
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CompareProductFilter


class RecommendationView(APIView):

    def get_similar_products_by_slug(self, product_slug=None):
        if product_slug is not None:
            try:
                product = get_object_or_404(Product, slug=product_slug)
                category = product.category
                similar_products = Product.objects.filter(category=category).exclude(slug=product.slug)
            except Http404:
                similar_products = Product.objects.all()
        else:
            similar_products = Product.objects.all()
        return similar_products

    def get(self, request, product_slug=None):
        try:
            if request.user.is_authenticated:
                cart = Cart.objects.filter(tep_user=request.user).first()
            else:
                ip_address = IPControlService(request, RedisDatabases.IP_CONTROL).get_ip()
                cart = Cart.objects.filter(ip_address=ip_address).first()

            cart_items = CartItem.objects.filter(cart=cart)
            cart_product_variants = cart_items.values_list('product_variants', flat=True)

            similar_products = Product.objects.filter(
                product_variants__in=cart_product_variants
            ).distinct()
            similar_products = similar_products.exclude(
                title__in=[item.product_variants.product.title for item in cart_items])

            if not similar_products.exists():
                similar_products = self.get_similar_products_by_slug(product_slug)

        except Cart.DoesNotExist:
            similar_products = self.get_similar_products_by_slug(product_slug)

        serializer = ProductSerializer(similar_products, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class InspirationImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InspirationImage.objects.all()
    serializer_class = InspirationImageSerializer
    authentication_classes = [IgnoreInvalidTokenAuthentication]
    permission_classes = [AllowAny]
    lookup_field = 'id'


class CategoryProductVariantViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategoryProductVariantSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_slug')
        products = Product.objects.filter(category__slug=category_id)
        return ProductVariant.objects.filter(product__in=products)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        data = serializer.aggregate_data(self.get_queryset())
        return Response(data)
