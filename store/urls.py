from django.urls import path
from .views import (
    ProductsImport,
    CategoryViewSet, ProductViewSet, SizeViewSet,
    ColorViewSet, MaterialViewSet, ProductVariantViewSet, ProductVariantInfoViewSet,
    ProductSearchViewSet
)

urlpatterns = [
    path('categories/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('categories/<slug:slug>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('products/', ProductViewSet.as_view({'get': 'list'})),
    path('products/import/', ProductsImport.as_view()),
    path('products/<slug:slug>/', ProductViewSet.as_view({'get': 'retrieve'})),
    path('products/search/', ProductSearchViewSet.as_view()),

    path('sizes/', SizeViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('sizes/<slug:slug>/', SizeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('colors/', ColorViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('colors/<slug:slug>/', ColorViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('materials/', MaterialViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('materials/<slug:slug>/', MaterialViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('variants/', ProductVariantViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('variants/<slug:slug>/', ProductVariantViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('variant-info/', ProductVariantInfoViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('variant-info/<slug:slug>/', ProductVariantInfoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]
