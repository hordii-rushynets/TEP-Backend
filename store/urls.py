from django.urls import path
from .views import (
    ProductsImport,
    CategoryViewSet, ProductViewSet, SizeViewSet,
    ColorViewSet, MaterialViewSet, ProductVariantViewSet, ProductVariantInfoViewSet
)

urlpatterns = [
    path('categories/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('categories/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('products/', ProductViewSet.as_view({'get': 'list'})),
    path('products/import/', ProductsImport.as_view()),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve'})),

    path('sizes/', SizeViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('sizes/<int:pk>/', SizeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('colors/', ColorViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('colors/<int:pk>/', ColorViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('materials/', MaterialViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('materials/<int:pk>/', MaterialViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('variants/', ProductVariantViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('variants/<int:pk>/', ProductVariantViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('variant-info/', ProductVariantInfoViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('variant-info/<int:pk>/', ProductVariantInfoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]
