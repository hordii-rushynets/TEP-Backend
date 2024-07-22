from .models import Vacancy
import django_filters
from store.filters import MultipleStringValuesFilter, BaseFilter


class VacancyFilter(BaseFilter):
    """Vacancy filter"""
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains')
    region = django_filters.CharFilter(field_name='region', lookup_expr='icontains')

    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')
    about_company = django_filters.CharFilter(field_name='about_company', lookup_expr='icontains')

    scope_of_work = MultipleStringValuesFilter(field_name='scope_of_work__name', lookup_expr='icontains')
    type_of_work = MultipleStringValuesFilter(field_name='type_of_work__name', lookup_expr='icontains')
    type_of_employment = MultipleStringValuesFilter(field_name='type_of_employment__name', lookup_expr='icontains')
    tag = MultipleStringValuesFilter(field_name='tag__name', lookup_expr='icontains')

    class Meta:
        model = Vacancy
        fields = ['title', 'city', 'region', 'description', 'about_company', 'scope_of_work', 'type_of_work',
                  'type_of_employment', 'tag']