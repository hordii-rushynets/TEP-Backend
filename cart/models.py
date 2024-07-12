from django.db import models
from store.models import ProductVariant
from tep_user.models import TEPUser


class Cart(models.Model):
    tep_user = models.OneToOneField(TEPUser, on_delete=models.CASCADE, related_name='tep_user')
    product_variants = models.ManyToManyField(ProductVariant, related_name='product_variants', blank=True)
