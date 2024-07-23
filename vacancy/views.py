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


class ScopeOfWorkViewSet(AbstractReadOnlyModelViewSet):
    """ScopeOfWork ViewSet"""
    queryset = ScopeOfWork.objects.all()
    serializer_class = ScopeOfWorkSerializer


class TypeOfWorkViewSet(AbstractReadOnlyModelViewSet):
    """TypeOfWork ViewSet"""
    queryset = TypeOfWork.objects.all()
    serializer_class = TypeOfWorkSerializer


class TypeOfEmploymentViewSet(AbstractReadOnlyModelViewSet):
    """TypeOfEmployment ViewSet"""
    queryset = TypeOfEmployment.objects.all()
    serializer_class = TypeOfEmploymentSerializer


class TagViewSet(AbstractReadOnlyModelViewSet):
    """Tag ViewSet"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class AddressViewSet(AbstractReadOnlyModelViewSet):
    """Address ViewSet"""
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
