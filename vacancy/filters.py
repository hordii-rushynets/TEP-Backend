from .models import Vacancy
import django_filters
from store.filters import MultipleStringValuesFilter


class VacancyFilter(django_filters.FilterSet):
    """Vacancy filter"""
    title_en = django_filters.CharFilter(field_name="title_en", lookup_expr='icontains')
    title_uk = django_filters.CharFilter(field_name="title_uk", lookup_expr='icontains')

    address_en = django_filters.CharFilter(field_name="address_en", lookup_expr='icontains')
    address_uk = django_filters.CharFilter(field_name="address_uk", lookup_expr='icontains')

    employment_type_en = django_filters.CharFilter(field_name="employment_type_en", lookup_expr='icontains')
    employment_type_uk = django_filters.CharFilter(field_name="employment_type_uk", lookup_expr='icontains')

    description_en = django_filters.CharFilter(field_name="description_en", lookup_expr='icontains')
    description_uk = django_filters.CharFilter(field_name="description_uk", lookup_expr='icontains')

    about_company_en = django_filters.CharFilter(field_name="about_company_en", lookup_expr='icontains')
    about_company_uk = django_filters.CharFilter(field_name="about_company_uk", lookup_expr='icontains')
    duties_en = MultipleStringValuesFilter("duties__value_en")
    duties_uk = MultipleStringValuesFilter("duties__value_uk")

    class Meta:
        model = Vacancy
        fields = ['title_en', 'title_uk', 'address_en', 'address_uk', 'employment_type_en', 'employment_type_uk',
                  'description_en', 'employment_type_uk', 'about_company_en', 'about_company_uk', 'duties_en',
                  'duties_uk']

    @property
    def qs(self):
        parent = super().qs
        return parent.distinct()
