from django.contrib import admin
from .models import Category, Post, Image, Section
# Register your models here.
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Section)
admin.site.register(Post)