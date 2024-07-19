from rest_framework import serializers
from .models import Vacancy
from store.serializers import FilterFieldSerializer, FilterField


class VacancySerializer(serializers.ModelSerializer):
    """Vacancy Serializer"""
    duties = FilterFieldSerializer(read_only=True, many=True)
    duties_ids = serializers.PrimaryKeyRelatedField(queryset=FilterField.objects.all(), many=True,
                                                          write_only=True, source='duties')

    class Meta:
        model = Vacancy
        fields = ['id', 'image', 'title', 'address', 'duties_ids', 'employment_type', 'description',
                  'about_company', 'duties']