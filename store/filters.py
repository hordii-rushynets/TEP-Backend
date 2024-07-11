import django_filters
from .models import Product, Category, ProductVariant
from django.db.models import Q


class MultipleValuesFilter(django_filters.BaseCSVFilter, django_filters.CharFilter):
    def filter(self, qs, value):
        if not value:
            return qs
        q_objects = Q()
        for val in value:
            q_objects |= Q(**{f"{self.field_name}__icontains": val})
        return qs.filter(q_objects)


class BaseFilter(django_filters.FilterSet):
    class Meta:
        abstract = True

    @property
    def qs(self):
        parent = super().qs
        return parent.distinct()


class ProductFilter(BaseFilter):
    slug = django_filters.CharFilter(field_name='slug', lookup_expr='icontains')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')

    price_min = django_filters.NumberFilter(field_name='product_variants__default_price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='product_variants__default_price', lookup_expr='lte')
    size = MultipleValuesFilter(field_name='product_variants__sizes__title')
    color = MultipleValuesFilter(field_name='product_variants__colors__title')
    material = MultipleValuesFilter(field_name='product_variants__materials__title')

    category_title = django_filters.CharFilter(field_name='category__title', lookup_expr='icontains')
    category_title_uk = django_filters.CharFilter(field_name='category__title_uk', lookup_expr='icontains')
    category_description = django_filters.CharFilter(field_name='category__description', lookup_expr='icontains')
    category_description_uk = django_filters.CharFilter(field_name='category__description_uk', lookup_expr='icontains')

    filter_fields_value_en_mul = MultipleValuesFilter(field_name='product_variants__filter_field__value_en')
    filter_fields_value_uk_mul = MultipleValuesFilter(field_name='product_variants__filter_field__value_uk')

    class Meta:
        model = Product
        fields = ['slug', 'title', 'description', 'price_min', 'price_max', 'size', 'color', 'material',
                  'category_title', 'category_title_uk', 'category_description', 'category_description_uk',
                  'filter_fields_value_en_mul', 'filter_fields_value_uk_mul']


class CategoryFilter(BaseFilter):
    title_en = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    title_uk = django_filters.CharFilter(field_name='title_uk', lookup_expr='icontains')
    description_en = django_filters.CharFilter(field_name='description', lookup_expr='icontains')
    description_uk = django_filters.CharFilter(field_name='description_uk', lookup_expr='icontains')

    filter_name = django_filters.CharFilter(field_name='filter__name')
    filter_name_uk = django_filters.CharFilter(field_name='filter__name_uk')
    filter_fields_value = django_filters.CharFilter(field_name='filter__filter_fields__value')
    filter_fields_value_uk = django_filters.CharFilter(field_name='filter__filter_fields__value_uk')

    class Meta:
        model = Category
        fields = ['title_en', 'title_uk', 'description_en', 'description_uk', 'filter_name', 'filter_name_uk',
                  'filter_fields_value', 'filter_fields_value_uk']


class ProductVariantFilter(BaseFilter):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')

    filter_fields_value = django_filters.CharFilter(field_name='filter_fields__value', lookup_expr='icontains')
    filter_fields_value_uk = django_filters.CharFilter(field_name='filter_fields__value_uk', lookup_expr='icontains')

    price_min = django_filters.NumberFilter(field_name='default_price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='default_price', lookup_expr='lte')

    promo_price_min = django_filters.NumberFilter(field_name='promo_price', lookup_expr='gte')
    promo_price_max = django_filters.NumberFilter(field_name='promo_price', lookup_expr='lte')

    class Meta:
        model = ProductVariant
        fields = ['title', 'filter_fields_value', 'filter_fields_value_uk', 'price_min', 'price_max',
                  'promo_price_min', 'promo_price_max']


