from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from transliterate import translit
from .tasks import import_data_task
from .models import Category, Product, Size, Color, Material, ProductVariant, ProductVariantInfo, Filter
from .serializers import (
    CategorySerializer, ProductSerializer, SizeSerializer,
    ColorSerializer, MaterialSerializer, ProductVariantSerializer,
    ProductVariantInfoSerializer, FilterSerializer, IncreaseNumberOfViewsSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter, CategoryFilter, ProductVariantFilter
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.request import Request


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
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter

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


@method_decorator(csrf_exempt, name='dispatch')
class ProductsImport(APIView):
    def post(self, request):
        data = request.data
        import_data_task.delay(data)
        return Response({'status': 'success'})