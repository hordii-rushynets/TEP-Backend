from rest_framework import serializers
from .models import Vacancy, ScopeOfWork, TypeOfWork, TypeOfEmployment, Tag


class ScopeOfWorkSerializer(serializers.ModelSerializer):
    """ScopeOfWork Serializer"""
    class Meta:
        model = ScopeOfWork
        fields = ['name']


class TypeOfWorkSerializer(serializers.ModelSerializer):
    """TypeOfWork Serializer"""
    class Meta:
        model = TypeOfWork
        fields = ['name']


class TypeOfEmploymentSerializer(serializers.ModelSerializer):
    """TypeOfEmployment Serializer"""
    class Meta:
        model = TypeOfEmployment
        fields = ['name']


class TagSerializer(serializers.ModelSerializer):
    """Tag Serializer"""
    class Meta:
        model = Tag
        fields = ['name']


class VacancySerializer(serializers.ModelSerializer):
    """Vacancy Serializer"""
    scope_of_work = ScopeOfWorkSerializer(read_only=True, many=True)
    type_of_work = TypeOfWorkSerializer(read_only=True, many=True)
    type_of_employment = TypeOfEmploymentSerializer(read_only=True, many=True)
    tag = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Vacancy
        fields = ['id', 'image', 'title', 'city', 'region', 'description', 'about_company',
                  'scope_of_work', 'type_of_work', 'type_of_employment', 'tag']
