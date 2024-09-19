from django.urls import path, include
from .views import (
    ProductsImport,
    CategoryViewSet, ProductViewSet, SizeViewSet,
    ColorViewSet, MaterialViewSet, ProductVariantViewSet, ProductVariantInfoViewSet, InspirationImageViewSet, 
    FilterViewSet, FavoriteProductViewset, FeedbackViewSet, FullDataViewSet, CompareProductViewSet, RecommendationView,
    CategoryProductVariantViewSet
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
router.register(r'feedback', FeedbackViewSet, basename='feedback')
router.register(r'full-data', FullDataViewSet, basename='full_data_product')
router.register(r'inspiration-image', InspirationImageViewSet, basename='inspiration_image')
router.register(r'compare', CompareProductViewSet, basename='compare')

urlpatterns = [
    path('import/', ProductsImport.as_view()),
    path('recommendation/', RecommendationView.as_view(), name='recommendation'),
    path('recommendation/<slug:product_slug>/', RecommendationView.as_view(), name='recommendations_with_slug'),
    path('categories-fields/<int:category_id>/', CategoryProductVariantViewSet.as_view({'get': 'list'}),
         name='category-product-variants'),
    path('', include(router.urls)),
]