from .models import Vacancy
import django_filters
from store.filters import MultipleStringValuesFilter, BaseFilter


class VacancyFilter(BaseFilter):
    """Vacancy filter"""
    title_en = django_filters.CharFilter(field_name='title_en', lookup_expr='icontains')
    title_uk = django_filters.CharFilter(field_name='title_uk', lookup_expr='icontains')
    title_ru = django_filters.CharFilter(field_name='title_ru', lookup_expr='icontains')

    city_en = django_filters.CharFilter(field_name='address__city_en', lookup_expr='icontains')
    region_en = django_filters.CharFilter(field_name='address__region_en', lookup_expr='icontains')

    city_uk = django_filters.CharFilter(field_name='address__city_uk', lookup_expr='icontains')
    region_uk = django_filters.CharFilter(field_name='address__region_uk', lookup_expr='icontains')

    city_ru = django_filters.CharFilter(field_name='address__city_ru', lookup_expr='icontains')
    region_ru = django_filters.CharFilter(field_name='address__region_ru', lookup_expr='icontains')

    description_en = django_filters.CharFilter(field_name='description_en', lookup_expr='icontains')
    about_company_en = django_filters.CharFilter(field_name='about_company_en', lookup_expr='icontains')

    description_uk = django_filters.CharFilter(field_name='description_uk', lookup_expr='icontains')
    about_company_uk = django_filters.CharFilter(field_name='about_company_uk', lookup_expr='icontains')

    description_ru = django_filters.CharFilter(field_name='description_ru', lookup_expr='icontains')
    about_company_ru = django_filters.CharFilter(field_name='about_company_ru', lookup_expr='icontains')

    scope_of_work_en = MultipleStringValuesFilter(field_name='scope_of_work__name_en')
    scope_of_work_uk = MultipleStringValuesFilter(field_name='scope_of_work__name_uk')
    scope_of_work_ru = MultipleStringValuesFilter(field_name='scope_of_work__name_ru')

    type_of_work_en = MultipleStringValuesFilter(field_name='type_of_work__name_en')
    type_of_work_uk = MultipleStringValuesFilter(field_name='type_of_work__name_uk')
    type_of_work_ru = MultipleStringValuesFilter(field_name='type_of_work__name_ru')

    type_of_employment_en = MultipleStringValuesFilter(field_name='type_of_employment__name_en')
    type_of_employment_uk = MultipleStringValuesFilter(field_name='type_of_employment__name_en')
    type_of_employment_ry = MultipleStringValuesFilter(field_name='type_of_employment__name_en')

    tag_en = MultipleStringValuesFilter(field_name='tag__name_en')
    tag_uk = MultipleStringValuesFilter(field_name='tag__name_uk')
    tag_ru = MultipleStringValuesFilter(field_name='tag__name_ru')

    class Meta:
        model = Vacancy
        fields = [
            'title_en', 'title_uk', 'title_ru',
            'city_en', 'region_en', 'city_uk', 'region_uk',
            'city_ru', 'region_ru', 'description_en', 'about_company_en',
            'description_uk', 'about_company_uk', 'description_ru', 'about_company_ru',
            'scope_of_work_en', 'scope_of_work_uk', 'scope_of_work_ru',
            'type_of_work_en', 'type_of_work_uk', 'type_of_work_ru',
            'type_of_employment_en', 'type_of_employment_uk', 'type_of_employment_ru',
            'tag_en', 'tag_uk', 'tag_ru'
        ]