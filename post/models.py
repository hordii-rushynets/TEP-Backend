from django.db import models

from store.models import ProductVariant
from tep_user.models import TEPUser


class Order(models.Model):
    UKRPOST = 'UkrPost'
    NOVAPOST = 'NovaPost'

    POST_TYPE_CHOICES = [
        (UKRPOST, 'UkrPost'),
        (NOVAPOST, 'NovaPost'),
    ]
    number = models.CharField(max_length=100)
    tep_user = models.ForeignKey(TEPUser, on_delete=models.CASCADE, related_name='orders')
    post_type = models.CharField(max_length=100, choices=POST_TYPE_CHOICES)
    product_variant = models.ManyToManyField(ProductVariant, related_name='orders')

    def __str__(self):
        return f"{self.post_type}: {self.number}"