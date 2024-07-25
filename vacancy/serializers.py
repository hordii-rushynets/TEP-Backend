from rest_framework import serializers
from .models import (Vacancy, ScopeOfWork, TypeOfWork, TypeOfEmployment, Tag, Address, CooperationOffer,
                     CooperationOfferFile)


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


class CooperationOfferSerializer(serializers.ModelSerializer):
    """Response To a Vacancy Serializer"""
    files = serializers.ListField(
        child=serializers.FileField(),  # Change to handle any file type
        write_only=True, required=False
    )

    class Meta:
        model = CooperationOffer
        fields = ['name', 'email', 'phone', 'message', 'vacancy', 'files']
        extra_kwargs = {
            'vacancy': {'required': False}
        }

    def validate(self, data):
        vacancy = data.get('vacancy')
        email = data.get('email')

        if vacancy and CooperationOffer.objects.filter(vacancy=vacancy, email=email).exists():
            raise serializers.ValidationError("You have already applied for this vacancy.")

        return data

    def create(self, validated_data):
        files_data = validated_data.pop('files', [])
        cooperation_offer = super().create(validated_data)

        for file_data in files_data:
            CooperationOfferFile.objects.create(cooperation_offer=cooperation_offer, file=file_data)

        return cooperation_offer
