from .models import Vacancy
import django_filters
from store.filters import MultipleStringValuesFilter, BaseFilter


class VacancyFilter(BaseFilter):
    """Vacancy filter"""
    title_en = django_filters.CharFilter(field_name='title_en', lookup_expr='icontains')
    title_uk = django_filters.CharFilter(field_name='title_uk', lookup_expr='icontains')
    title_ru = django_filters.CharFilter(field_name='title_ru', lookup_expr='icontains')

    city = django_filters.CharFilter(field_name='address__city', lookup_expr='icontains')
    region = django_filters.CharFilter(field_name='address__region', lookup_expr='icontains')

    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')
    about_company = django_filters.CharFilter(field_name='about_company', lookup_expr='icontains')

    scope_of_work = MultipleStringValuesFilter(field_name='scope_of_work__name')

    type_of_work = MultipleStringValuesFilter(field_name='type_of_work__name')

    type_of_employment = MultipleStringValuesFilter(field_name='type_of_employment__name')

    tag = MultipleStringValuesFilter(field_name='tag__name')

    class Meta:
        model = Vacancy
        fields = ['title_en', 'title_uk', 'title_ru', 'city', 'region', 'description', 'about_company',
                  'scope_of_work', 'type_of_work', 'type_of_employment', 'tag']
