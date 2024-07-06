from django.urls import path
from .views import (
    BlogCategoryViewSet, BlogPostViewSet
)

urlpatterns = [
    path('categories/', BlogCategoryViewSet.as_view({'get': 'list'})),
    path('posts/', BlogPostViewSet.as_view({'get': 'list'})),
    path('post/<slug:slug>/', BlogPostViewSet.as_view({'get': 'retrieve'})),
]
