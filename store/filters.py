import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    slug = django_filters.CharFilter(field_name='slug', lookup_expr='icontains')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__title', lookup_expr='icontains')
    price_min = django_filters.NumberFilter(field_name='productvariant__default_price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='productvariant__default_price', lookup_expr='lte')
    size = django_filters.CharFilter(field_name='productvariant__sizes__title', lookup_expr='icontains')
    color = django_filters.CharFilter(field_name='productvariant__colors__title', lookup_expr='icontains')
    material = django_filters.CharFilter(field_name='productvariant__materials__title', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['slug', 'title', 'category', 'price_min', 'price_max', 'size', 'color', 'material']
