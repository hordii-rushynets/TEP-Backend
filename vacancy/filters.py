from .models import Vacancy
import django_filters
from store.filters import MultipleStringValuesFilter


class VacancyFilter(django_filters.FilterSet):
    """Vacancy filter"""
    title = django_filters.CharFilter(field_name="title", lookup_expr='icontains')
    address = django_filters.CharFilter(field_name="address", lookup_expr='icontains')
    employment_type = django_filters.CharFilter(field_name="employment_type", lookup_expr='icontains')
    description = django_filters.CharFilter(field_name="description", lookup_expr='icontains')
    about_company = django_filters.CharFilter(field_name="about_company", lookup_expr='icontains')
    duties_en = MultipleStringValuesFilter("duties__value_en")
    duties_uk = MultipleStringValuesFilter("duties__value_uk")

    class Meta:
        model = Vacancy
        fields = ['title', 'address', 'employment_type', 'description', 'about_company', 'duties']

    @property
    def qs(self):
        parent = super().qs
        return parent.distinct()
