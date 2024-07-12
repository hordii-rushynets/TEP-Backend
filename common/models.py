"""Contains model abstractions to use in other apps."""
from django.db import models


class TitleSlug(models.Model):
    """Abstract model that contain title and slug fied."""
    slug = models.CharField(max_length=128)
    title = models.CharField(max_length=128)

    class Meta:
        abstract = True
