import django_filters
from .models import Product, Category, ProductVariant


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

    class Meta:
        model = Product
        fields = ['slug', 'title', 'price_min', 'price_max', 'size', 'color', 'material', 'category_title',
                  'category_title_uk', 'category_description', 'category_description_uk']

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


class ProductVariantFilter(django_filters.FilterSet):
    product = django_filters.CharFilter(field_name='product__slug', lookup_expr='icontains')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    sku = django_filters.CharFilter(field_name='sku', lookup_expr='icontains')
    default_price_min = django_filters.NumberFilter(field_name='default_price', lookup_expr='gte')
    default_price_max = django_filters.NumberFilter(field_name='default_price', lookup_expr='lte')
    wholesale_price_min = django_filters.NumberFilter(field_name='wholesale_price', lookup_expr='gte')
    wholesale_price_max = django_filters.NumberFilter(field_name='wholesale_price', lookup_expr='lte')
    drop_shipping_price_min = django_filters.NumberFilter(field_name='drop_shipping_price', lookup_expr='gte')
    drop_shipping_price_max = django_filters.NumberFilter(field_name='drop_shipping_price', lookup_expr='lte')
    size = django_filters.CharFilter(field_name='sizes__title', lookup_expr='icontains')
    color = django_filters.CharFilter(field_name='colors__title', lookup_expr='icontains')
    material = django_filters.CharFilter(field_name='materials__title', lookup_expr='icontains')
    promotion = django_filters.BooleanFilter(field_name='promotion')
    promo_price_min = django_filters.NumberFilter(field_name='promo_price', lookup_expr='gte')
    promo_price_max = django_filters.NumberFilter(field_name='promo_price', lookup_expr='lte')
    count_min = django_filters.NumberFilter(field_name='count', lookup_expr='gte')
    count_max = django_filters.NumberFilter(field_name='count', lookup_expr='lte')
    variant_order_min = django_filters.NumberFilter(field_name='variant_order', lookup_expr='gte')
    variant_order_max = django_filters.NumberFilter(field_name='variant_order', lookup_expr='lte')
    filter_name = django_filters.CharFilter(field_name='filter__name', lookup_expr='icontains')
    filter_name_uk = django_filters.CharFilter(field_name='filter__name_uk', lookup_expr='icontains')
    filter_fields_value = django_filters.CharFilter(field_name='filter__filter_fields__value',
                                                        lookup_expr='icontains')
    filter_fields_value_uk = django_filters.CharFilter(field_name='filter__filter_fields__value_uk',
                                                           lookup_expr='icontains')

    class Meta:
        model = ProductVariant
        fields = [
            'product', 'title', 'sku', 'default_price_min', 'default_price_max', 'wholesale_price_min',
            'wholesale_price_max', 'drop_shipping_price_min', 'drop_shipping_price_max', 'size', 'color', 'material',
            'promotion', 'promo_price_min', 'promo_price_max', 'count_min', 'count_max', 'variant_order_min',
            'variant_order_max', 'filter_name', 'filter_name_uk', 'filter_fields_value', 'filter_fields_value_uk'
        ]

    @property
    def qs(self):
        parent = super().qs
        return parent.distinct()

