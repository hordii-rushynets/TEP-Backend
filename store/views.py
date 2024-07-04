from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from transliterate import translit
from .tasks import import_data_task
from .models import Category, Product, Size, Color, Material, ProductVariant, ProductVariantInfo
from .serializers import (
    CategorySerializer, ProductSerializer, SizeSerializer,
    ColorSerializer, MaterialSerializer, ProductVariantSerializer, ProductVariantInfoSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter, CategoryFilter



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


class ProductVariantInfoViewSet(viewsets.ModelViewSet):
    queryset = ProductVariantInfo.objects.all()
    serializer_class = ProductVariantInfoSerializer
    lookup_field = 'slug'


@method_decorator(csrf_exempt, name='dispatch')
class ProductsImport(APIView):
    def post(self, request):
        data = request.data
        import_data_task.delay(data)
        return Response({'status': 'success'})