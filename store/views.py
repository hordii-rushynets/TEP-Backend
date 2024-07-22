from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from transliterate import translit
from .tasks import import_data_task
from .models import (Category, Product, Size, Color, Material, ProductVariant,
                     ProductVariantInfo, Filter, FavoriteProduct, Feedback, FeedbackImage)
from .serializers import (
    CategorySerializer, ProductSerializer, SizeSerializer,
    ColorSerializer, MaterialSerializer, ProductVariantSerializer,
    ProductVariantInfoSerializer, FilterSerializer, IncreaseNumberOfViewsSerializer,
    SetFavoriteProductSerializer, FeedbackSerializer
)
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter, CategoryFilter, ProductVariantFilter, FeedbackFilter
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.request import Request
from django.db.models import QuerySet, Count
from rest_framework.filters import OrderingFilter


def generate_latin_slug(string):
    latin_string = translit(string, 'uk', reversed=True)
    clean_string = ''.join(e for e in latin_string if e.isalnum() or e == ' ')
    slug = clean_string.replace(' ', '-').lower()
    return slug


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CategoryFilter


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ProductFilter
    ordering_fields = ['number_of_views', 'number_of_add_to_cart']
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


class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    lookup_field = 'slug'


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    lookup_field = 'slug'


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    lookup_field = 'slug'


class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductVariantFilter


class ProductVariantInfoViewSet(viewsets.ModelViewSet):
    queryset = ProductVariantInfo.objects.all()
    serializer_class = ProductVariantInfoSerializer
    lookup_field = 'slug'


class FilterViewSet(viewsets.ModelViewSet):
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
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FeedbackFilter

    def get_queryset(self):
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        """List the objects of the queryset."""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single object instance."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new object instance."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        feedback = serializer.save(tep_user=self.request.user)

        # Handle feedback_images if they are sent in the request
        images = request.FILES.getlist('feedback_images')
        for image in images:
            FeedbackImage.objects.create(feedback=feedback, image=image)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def like_dislike(self, request, *args, **kwargs):
        """Handle like and dislike functionality."""
        feedback = self.get_object()
        user = request.user

        existing_feedback = Feedback.objects.filter(
            tep_user=user,
            product=feedback.product
        ).first()

        if existing_feedback:
            if existing_feedback.like_number > 0:
                existing_feedback.like_number -= 1
                existing_feedback.save()
            elif existing_feedback.dislike_number > 0:
                existing_feedback.dislike_number -= 1
                existing_feedback.save()

        action_type = request.data.get('action')

        if action_type == 'like':
            feedback.like_number += 1
        elif action_type == 'dislike':
            feedback.dislike_number += 1
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

        feedback.save()

        return Response({
            'like_number': feedback.like_number,
            'dislike_number': feedback.dislike_number
        })


@method_decorator(csrf_exempt, name='dispatch')
class ProductsImport(APIView):
    def post(self, request):
        data = request.data
        import_data_task.delay(data)
        return Response({'status': 'success'})