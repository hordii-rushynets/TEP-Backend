from django.db import models
from tep_user.models import TEPUser
from store.models import ProductVariant


class Order(models.Model):
    number = models.CharField(max_length=100)
    tep_user = models.ForeignKey(TEPUser, on_delete=models.CASCADE, related_name='orders')
    post_type = models.CharField(max_length=100)
    product_variant = models.ManyToManyField(ProductVariant, related_name='orders')

    def __str__(self):
        return f"{self.post_type}: {self.number}"