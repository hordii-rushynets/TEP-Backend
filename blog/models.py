from django.conf import settings
from django.db import models

from common.models import TitleSlug

from ckeditor.fields import RichTextField


class Tag(TitleSlug):
    description = RichTextField(max_length=30000, blank=True, null=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.title


class Post(TitleSlug):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)
    meta_description = RichTextField(max_length=30000)
    image = models.ImageField(blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Complexity(models.Model):
    photo = models.ImageField(upload_to='complexity_images/', blank=True, null=True)
    title = models.CharField(max_length=128)
    description = RichTextField(max_length=30000)
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='complexity')

    def __str__(self):
        return self.title


class Requirements(models.Model):
    title = models.CharField(max_length=128)
    description = RichTextField(max_length=30000)
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='requirements')

    def __str__(self):
        return self.title


class Materials(models.Model):
    title = models.CharField(max_length=128)
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='what_materials')
    photo = models.ImageField(upload_to='what_materials_images/', blank=True, null=True)
    description = RichTextField(max_length=30000, blank=True, null=True)

    def __str__(self):
        return self.title


class ForChildren(models.Model):
    photo = models.ImageField(upload_to='for_children_images/', blank=True, null=True)
    description = RichTextField(max_length=30000)
    additional_description = RichTextField(max_length=30000)
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='for_children')

    def __str__(self):
        return self.description
