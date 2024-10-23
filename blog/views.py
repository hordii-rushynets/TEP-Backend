from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import viewsets

from .pagination import PostPagination
from .models import Tag, Post
from .serializers import TagSerializer, PostSerializer


@method_decorator(cache_page(60 * 60 * 3), name='dispatch')
class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'


@method_decorator(cache_page(60 * 60 * 3), name='dispatch')
class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    pagination_class = PostPagination
