from django.conf import settings
from django.db import models

from common.models import TitleSlug


class Tag(TitleSlug):
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.title


class Post(TitleSlug):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)
    meta_description = models.TextField()
    image = models.ImageField(blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Section(models.Model):
    SECTION_TYPES = (
        ('complexity', 'Complexity'),
        ('requirements', 'Requirements'),
        ('what_materials', 'Materials'),
        ('for_children', 'For children'),
    )

    types = models.CharField(choices=SECTION_TYPES, default=SECTION_TYPES[0][0])
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='section')
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    additional_description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.title}"
