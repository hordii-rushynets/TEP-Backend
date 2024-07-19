from .views import VacancyViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', VacancyViewSet, basename='vacancy')

urlpatterns = router.urls + []
