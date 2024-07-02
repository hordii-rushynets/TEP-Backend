import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__title', lookup_expr='icontains')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')
    group_id = django_filters.CharFilter(field_name='group_id', lookup_expr='icontains')
    variant_title = django_filters.CharFilter(field_name='productvariant__title', lookup_expr='icontains')
    variant_sku = django_filters.CharFilter(field_name='productvariant__sku', lookup_expr='icontains')
    size = django_filters.CharFilter(field_name='productvariant__sizes__title', lookup_expr='icontains')
    color = django_filters.CharFilter(field_name='productvariant__colors__title', lookup_expr='icontains')
    material = django_filters.CharFilter(field_name='productvariant__materials__title', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = [
            'category', 'title', 'description', 'group_id',
            'variant_title', 'variant_sku', 'size', 'color', 'material'
        ]
