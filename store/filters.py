import django_filters
from .models import Product, Category


class ProductFilter(django_filters.FilterSet):
    slug = django_filters.CharFilter(field_name='slug', lookup_expr='icontains')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')

    price_min = django_filters.NumberFilter(field_name='productvariant__default_price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='productvariant__default_price', lookup_expr='lte')
    size = django_filters.CharFilter(field_name='productvariant__sizes__title', lookup_expr='icontains')
    color = django_filters.CharFilter(field_name='productvariant__colors__title', lookup_expr='icontains')
    material = django_filters.CharFilter(field_name='productvariant__materials__title', lookup_expr='icontains')

    category_title = django_filters.CharFilter(field_name='category__title', lookup_expr='icontains')
    category_title_uk = django_filters.CharFilter(field_name='category__title_uk', lookup_expr='icontains')
    category_description = django_filters.CharFilter(field_name='category__description', lookup_expr='icontains')
    category_description_uk = django_filters.CharFilter(field_name='category__description_uk', lookup_expr='icontains')

    filter_name = django_filters.CharFilter(field_name='filter__name', lookup_expr='icontains')
    filter_name_uk = django_filters.CharFilter(field_name='filter__name_uk', lookup_expr='icontains')

    filter_fields_value = django_filters.CharFilter(field_name='filter__filter_fields__value', lookup_expr='icontains')
    filter_fields_value_uk = django_filters.CharFilter(field_name='filter__filter_fields__value_uk', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['slug', 'title', 'price_min', 'price_max', 'size', 'color', 'material', 'category_title',
                  'category_title_uk', 'category_description', 'category_description_uk', 'filter_name',
                  'filter_fields_value']

    @property
    def qs(self):
        parent = super().qs
        return parent.distinct()


class CategoryFilter(django_filters.FilterSet):
    slug = django_filters.CharFilter(field_name='slug', lookup_expr='icontains')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    title_uk = django_filters.CharFilter(field_name='title_uk', lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')
    description_uk = django_filters.CharFilter(field_name='description_uk', lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['slug', 'title', 'title_uk', 'description', 'description_uk']

    @property
    def qs(self):
        parent = super().qs
        return parent.distinct()

