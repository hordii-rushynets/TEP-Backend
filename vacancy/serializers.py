from rest_framework import serializers
from .models import Vacancy, ScopeOfWork, TypeOfWork, TypeOfEmployment, Tag, Address, ResponseToVacancy


class ScopeOfWorkSerializer(serializers.ModelSerializer):
    """ScopeOfWork Serializer"""
    class Meta:
        model = ScopeOfWork
        fields = ['id', 'name', "name_uk", "name_en", "name_ru"]


class TypeOfWorkSerializer(serializers.ModelSerializer):
    """TypeOfWork Serializer"""
    class Meta:
        model = TypeOfWork
        fields = '__all__'


class TypeOfEmploymentSerializer(serializers.ModelSerializer):
    """TypeOfEmployment Serializer"""
    class Meta:
        model = TypeOfEmployment
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """Tag Serializer"""
    class Meta:
        model = Tag
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    """Address Serializer"""
    class Meta:
        model = Address
        fields = '__all__'


class VacancySerializer(serializers.ModelSerializer):
    """Vacancy Serializer"""
    scope_of_work = ScopeOfWorkSerializer(read_only=True, many=True)
    type_of_work = TypeOfWorkSerializer(read_only=True, many=True)
    type_of_employment = TypeOfEmploymentSerializer(read_only=True, many=True)
    tag = TagSerializer(read_only=True, many=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Vacancy
        fields = '__all__'


class FullDataSerializer(serializers.Serializer):
    scope_of_work = ScopeOfWorkSerializer(read_only=True, many=True)
    type_of_work = TypeOfWorkSerializer(read_only=True, many=True)
    type_of_employment = TypeOfEmploymentSerializer(read_only=True, many=True)
    tag = TagSerializer(read_only=True, many=True)
    address = AddressSerializer(read_only=True, many=True)

    class Meta:
        model = Vacancy
        fields = ['scope_of_work', 'type_of_work', 'type_of_employment', 'tag', 'address']


class ResponseToVacancySerializer(serializers.ModelSerializer):
    """Response To a Vacancy Serializer"""

    vacancy = VacancySerializer(read_only=True)
    vacancy_id = serializers.PrimaryKeyRelatedField(
        queryset=Vacancy.objects.all(), source='vacancy', write_only=True)

    class Meta:
        model = ResponseToVacancy
        fields = ['name', 'email', 'phone', 'message', 'vacancy', 'vacancy_id']
