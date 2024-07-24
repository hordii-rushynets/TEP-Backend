from rest_framework import viewsets
from .models import Vacancy, ScopeOfWork, TypeOfWork, TypeOfEmployment, Tag, Address
from .serializers import (VacancySerializer, ScopeOfWorkSerializer, TypeOfWorkSerializer, TypeOfEmploymentSerializer,
                          TagSerializer, AddressSerializer)
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .filters import VacancyFilter


class AbstractReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    """Abstract ReadOnly Model"""
    permission_classes = [AllowAny]
    lookup_field = 'id'


class VacancyViewSet(viewsets.ReadOnlyModelViewSet):
    """Vacancy ViewSet"""
    queryset = Vacancy.objects.all()
    permission_classes = [AllowAny]
    serializer_class = VacancySerializer
    pagination_class = None
    lookup_field = 'id'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = VacancyFilter


class ScopeOfWorkViewSet(viewsets.ReadOnlyModelViewSet):
    """ScopeOfWork ViewSet"""
    queryset = ScopeOfWork.objects.all()
    serializer_class = ScopeOfWorkSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'


class TypeOfWorkViewSet(viewsets.ReadOnlyModelViewSet):
    """TypeOfWork ViewSet"""
    queryset = TypeOfWork.objects.all()
    serializer_class = TypeOfWorkSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'


class TypeOfEmploymentViewSet(viewsets.ReadOnlyModelViewSet):
    """TypeOfEmployment ViewSet"""
    queryset = TypeOfEmployment.objects.all()
    serializer_class = TypeOfEmploymentSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Tag ViewSet"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'


class AddressViewSet(viewsets.ReadOnlyModelViewSet):
    """Address ViewSet"""
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
