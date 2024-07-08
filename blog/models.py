from django.utils import timezone
from django.db import models
from django.conf import settings


class Category(models.Model):
    slug = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    slug = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    categories = models.ManyToManyField('Category', related_name='posts', blank=True)
    meta_description = models.TextField()
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.title


class Section(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='section')
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return f"{self.title}"


class Image(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='blog_images/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.section.title} Image"