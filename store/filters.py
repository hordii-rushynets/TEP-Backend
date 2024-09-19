from .models import Product, Category, ProductVariant, Feedback
from typing import List, Optional
import django_filters
from django.db.models import Q, QuerySet


class MultipleStringValuesFilter(django_filters.BaseCSVFilter, django_filters.CharFilter):
    """
    A custom filter class to filter querysets based on multiple string values.

    This filter extends BaseCSVFilter and CharFilter from django_filters to allow
    filtering of querysets where the specified field contains any of the provided values.

    Attributes:
        field_name (str): The name of the field to filter on.
    """

    def filter(self, qs: QuerySet, value: Optional[List[str]]) -> QuerySet:
        """
        Filters the queryset based on multiple string values.

        Args:
            qs (QuerySet): The initial queryset to filter.
            value (Optional[List[str]]): A list of string values to filter the queryset.

        Returns:
            QuerySet: The filtered queryset.
        """
        if not value:
            return qs

        q_objects = Q()
        for val in value:
            q_objects |= Q(**{f"{self.field_name}__icontains": val})

        return qs.filter(q_objects)


class MultipleNumberValuesFilter(django_filters.BaseCSVFilter, django_filters.NumberFilter):
    """
    A custom filter class to filter querysets based on multiple number values.

    This filter extends BaseCSVFilter and NumberFilter from django_filters to allow
    filtering of querysets where the specified field contains any of the provided values.

    Attributes:
        field_name (str): The name of the field to filter on.
    """

    def filter(self, qs: QuerySet, value: Optional[List[int | float]]) -> QuerySet:
        """
        Filters the queryset based on multiple CSV values.

        Args:
            qs (QuerySet): The initial queryset to filter.
            value (Optional[List[str]]): A list of string values to filter the queryset.

        Returns:
            QuerySet: The filtered queryset.
        """
        if not value:
            return qs

        q_objects = Q()
        for val in value:
            q_objects |= Q(**{f"{self.field_name}": val})

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
    title_en = django_filters.CharFilter(field_name='title_en', lookup_expr='icontains')
    title_uk = django_filters.CharFilter(field_name='title_uk', lookup_expr='icontains')
    title_ru = django_filters.CharFilter(field_name='title_ru', lookup_expr='icontains')

    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')

    price_min = django_filters.NumberFilter(field_name='product_variants__default_price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='product_variants__default_price', lookup_expr='lte')
    size = MultipleStringValuesFilter(field_name='product_variants__sizes__title')
    color = MultipleStringValuesFilter(field_name='product_variants__colors__title')
    material = MultipleStringValuesFilter(field_name='product_variants__materials__title')

    promo_price_min = django_filters.NumberFilter(method='filter_promo_price_min')
    promo_price_max = django_filters.NumberFilter(method='filter_promo_price_max')
    is_promotion = django_filters.BooleanFilter(field_name='product_variants__promotion')

    category_slug = django_filters.CharFilter(field_name='category__slug', lookup_expr='icontains')
    category_title = django_filters.CharFilter(field_name='category__title', lookup_expr='icontains')
    category_title_uk = django_filters.CharFilter(field_name='category__title_uk', lookup_expr='icontains')
    category_description = django_filters.CharFilter(field_name='category__description', lookup_expr='icontains')
    category_description_uk = django_filters.CharFilter(field_name='category__description_uk', lookup_expr='icontains')

    filter_fields_value_en = MultipleStringValuesFilter(field_name='product_variants__filter_field__value_en')
    filter_fields_value_uk = MultipleStringValuesFilter(field_name='product_variants__filter_field__value_uk')
    filter_fields_id = MultipleNumberValuesFilter(field_name='product_variants__filter_field__id')

    time = django_filters.OrderingFilter(fields=[('last_modified', 'faster'), ('-last_modified', 'later')])

    ordering = django_filters.OrderingFilter(
        fields=(
            ('number_of_views', 'number_of_views'),
            ('number_of_add_to_cart', 'number_of_add_to_cart'),
        ),
        field_labels={
            'number_of_views': 'Number of Views',
            'number_of_add_to_cart': 'Number of Add to Cart',
        }
    )

    class Meta:
        model = Product
        fields = [
            'slug', 'title', 'description', 'price_min', 'price_max', 'size', 'color', 'material',
            'promo_price_min', 'promo_price_max', 'is_promotion', 'category_slug', 'category_title',
            'category_title_uk', 'category_description', 'category_description_uk', 'filter_fields_value_en',
            'filter_fields_value_uk', 'filter_fields_id', 'time']

    def filter_promo_price_min(self, queryset, name, value):
        return queryset.filter(product_variants__promotion=True, product_variants__promo_price__gte=value)

    def filter_promo_price_max(self, queryset, name, value):
        return queryset.filter(product_variants__promotion=True, product_variants__promo_price__lte=value)


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

    promo_price_min = django_filters.NumberFilter(field_name='promo_price', method='filter_promo_price_min')
    promo_price_max = django_filters.NumberFilter(field_name='promo_price', method='filter_promo_price_max')

    class Meta:
        model = ProductVariant
        fields = ['title', 'filter_fields_value', 'filter_fields_value_uk', 'price_min', 'price_max',
                  'promo_price_min', 'promo_price_max']

    def filter_promo_price_min(self, queryset, name, value):
        return queryset.filter(promotion=True, promo_price__gte=value)

    def filter_promo_price_max(self, queryset, name, value):
        return queryset.filter(promotion=True, promo_price__lte=value)


class FeedbackFilter(BaseFilter):
    """Feedback Filter"""
    user_id = django_filters.NumberFilter(field_name='tep_user__id')
    user_email = django_filters.CharFilter(field_name='tep_user__email', lookup_expr='icontains')

    product = django_filters.CharFilter(field_name='product__slug', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='product__category__slug', lookup_expr='icontains')

    text = django_filters.CharFilter(field_name='text', lookup_expr='icontains')
    like_number_min = django_filters.NumberFilter(field_name='like_number', lookup_expr='gte')
    like_number_max = django_filters.NumberFilter(field_name='like_number', lookup_expr='lte')

    dislike_number_min = django_filters.NumberFilter(field_name='dislike_number', lookup_expr='gte')
    dislike_number_max = django_filters.NumberFilter(field_name='dislike_number', lookup_expr='lte')

    evaluation = MultipleNumberValuesFilter(field_name='evaluation')

    class Meta:
        model = Feedback
        fields = ['user_id', 'user_email', 'product', 'category', 'text', 'like_number_min', 'like_number_max',
                  'dislike_number_min', 'dislike_number_max', 'evaluation']


class CompareProductFilter(BaseFilter):
    ids = MultipleNumberValuesFilter(field_name="id")

    class Meta:
        model = Product
        fields = ['ids']
