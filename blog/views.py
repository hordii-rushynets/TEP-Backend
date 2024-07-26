from rest_framework import viewsets
from .pagination import PostPagination
from .models import Tag, Post
from .serializers import TagSerializer, PostSerializer


class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    pagination_class = PostPagination
