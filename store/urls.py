from django.urls import path, include
from .views import (
    ProductsImport,
    CategoryViewSet, ProductViewSet, SizeViewSet,
    ColorViewSet, MaterialViewSet, ProductVariantViewSet, ProductVariantInfoViewSet,
    FilterViewSet, FavoriteProductViewset
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'products/favorite', FavoriteProductViewset, basename='favorite-products')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'sizes', SizeViewSet, basename='sizes')
router.register(r'colors', ColorViewSet, basename='colors')
router.register(r'materials', MaterialViewSet, basename='materials')
router.register(r'variants', ProductVariantViewSet, basename='variants')
router.register(r'variant-info', ProductVariantInfoViewSet, basename='variant-info')
router.register(r'filters', FilterViewSet, basename='filters')

urlpatterns = [
    path('', include(router.urls)),
    path('products/import/', ProductsImport.as_view()),
]