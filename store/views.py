from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.request import Request
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin

from django.core.cache import cache
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
    CategoryProductVariantSerializer, update_cache_is_favorite_status
)
from .filters import ProductFilter, CategoryFilter, ProductVariantFilter, FeedbackFilter, CompareProductFilter
from .until import get_auth_date

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
        limit = self.request.query_params.get('limit')

        if limit and limit.isdigit():
            limit = int(limit)
            product = Product.objects.all()[:limit].values_list('id', flat=True)
            return Product.objects.filter(id__in=product).annotate(
                number_of_add_to_cart=Count('product_variants__cart_item'))

        return Product.objects.annotate(
                number_of_add_to_cart=Count('product_variants__cart_item')
        )

    def list(self, request, *args, **kwargs):
        user_data = get_auth_date(request)
        url = str(request.build_absolute_uri()).split('api')[1]
        cache_key = f'user-{user_data}-url-{url}'
        cache_key_to_url = f'user-{user_data}-urls'

        cache_data = cache.get(cache_key)

        if cache_data is None:
            serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
            cache.set(cache_key, serializer.data, timeout=3600)
            return Response(serializer.data)

        cache_keys_data = cache.get(cache_key_to_url)
        if cache_keys_data is None:
            keys = set(cache_key)
            cache.set(cache_key_to_url, keys, timeout=3600)
        else:
            keys = set(cache_keys_data)
            keys.add(cache_key)
            cache.set(cache_key_to_url, keys, timeout=3600)

        return Response(cache_data)

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


class FavoriteProductViewset(CreateModelMixin, ListModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    authentication_classes = [IgnoreInvalidTokenAuthentication]
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        serializers = {
            'create': SetFavoriteProductSerializer,
            'list': ProductSerializer
        }
        return serializers[self.action]

    def get_queryset(self) -> QuerySet:
        """Return products that are marked as favorite."""
        request = self.request

        ip_control_service = IPControlService(request=request, database=RedisDatabases.IP_CONTROL)
        favorite_products = FavoriteProduct.objects.filter(favorite=True)

        if request.user.is_authenticated:
            products = favorite_products.filter(user=request.user)
        else:
            products = favorite_products.filter(ip_address=ip_control_service.get_ip())

        return Product.objects.filter(id__in=products.values_list('product__id', flat=True))

    def destroy(self, request: Request, *args, **kwargs):
        """Remove all products from favorites."""
        ip_control_service = IPControlService(request=request, database=RedisDatabases.IP_CONTROL)
        if request.user.is_authenticated:
            favorite_products, _ = FavoriteProduct.objects.filter(user=request.user)
        else:
            favorite_products, _ = FavoriteProduct.objects.filter(ip_address=ip_control_service.get_ip())

        for favorite_product in favorite_products:
            update_cache_is_favorite_status(request, favorite_product.product, False)
            favorite_product.delete()

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
    authentication_classes = [IgnoreInvalidTokenAuthentication]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
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
    def get(self, request, product_slug=None):
        """Handles the GET request."""
        queryset = self.get_queryset(request, product_slug)
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self, request, product_slug=None):
        """Generates a queryset of similar products."""
        cart = self.get_cart(request)
        cart_items = self.get_cart_items(cart)

        similar_products = self.get_similar_products_by_cart(cart_items)

        if not similar_products.exists():
            similar_products = self.get_similar_products_by_slug(product_slug)

        return self.apply_limit(similar_products, request)

    def get_cart(self, request):
        """Retrieves the user's cart or by IP address."""
        if request.user.is_authenticated:
            return Cart.objects.filter(tep_user=request.user).first()
        else:
            ip_address = IPControlService(request, RedisDatabases.IP_CONTROL).get_ip()
            return Cart.objects.filter(ip_address=ip_address).first()

    def get_cart_items(self, cart):
        """Retrieves all items from the cart."""
        return CartItem.objects.filter(cart=cart) if cart else CartItem.objects.none()

    def get_similar_products_by_cart(self, cart_items):
        """Retrieves products similar to those in the cart."""
        cart_product_variants = cart_items.values_list('product_variants', flat=True)
        similar_products = Product.objects.filter(product_variants__in=cart_product_variants).distinct()
        excluded_titles = cart_items.values_list('product_variants__product__title', flat=True)
        return similar_products.exclude(title__in=excluded_titles)

    def get_similar_products_by_slug(self, product_slug=None):
        """Retrieves products similar to the current one based on its category."""
        if product_slug:
            product = get_object_or_404(Product, slug=product_slug)
            return Product.objects.filter(category=product.category).exclude(slug=product.slug)
        return Product.objects.all()

    def apply_limit(self, queryset, request):
        """Applies a limit on the number of products."""
        limit = request.query_params.get('limit')
        if limit and limit.isdigit():
            return queryset[:int(limit)]
        return queryset


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