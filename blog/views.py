from rest_framework import viewsets
from .models import Category, Post
from .serializers import CategorySerializer
# Create your views here.


class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

