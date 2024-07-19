from rest_framework import viewsets
from .models import Vacancy
from .serializers import VacancySerializer
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .filters import VacancyFilter


class VacancyViewSet(viewsets.ReadOnlyModelViewSet):
    """Vacancy ViewSet"""
    queryset = Vacancy.objects.all()
    permission_classes = [AllowAny]
    serializer_class = VacancySerializer
    pagination_class = None
    lookup_field = 'id'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = VacancyFilter
