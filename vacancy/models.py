from django.db import models
from store.models import FilterField


class Vacancy(models.Model):
    """Vacancy Model"""
    image = models.ImageField(upload_to='vacancy/images/', blank=True)
    title = models.TextField()
    address = models.TextField()
    employment_type = models.TextField()
    description = models.TextField()
    about_company = models.TextField()
    duties = models.ManyToManyField(FilterField, related_name='vacancy')


