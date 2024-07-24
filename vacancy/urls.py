from .views import (VacancyViewSet, ScopeOfWorkViewSet, TypeOfWorkViewSet, TypeOfEmploymentViewSet,
                    TagViewSet, AddressViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', VacancyViewSet, basename='vacancy')
router.register(r'scope-of-work', ScopeOfWorkViewSet, basename='scope_of_work')
router.register(r'type-of-work', TypeOfWorkViewSet, basename='type_of_work')
router.register(r'type-of-employment', TypeOfEmploymentViewSet, basename='type_of_employment')
router.register(r'tag', TagViewSet, basename='tag')
router.register(r'address', AddressViewSet, basename='address')


urlpatterns = router.urls + []
