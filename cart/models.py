from django.db import models
from store.models import ProductVariant, Color, Material, Size, FilterField
from tep_user.models import TEPUser


class Cart(models.Model):
    tep_user = models.OneToOneField(TEPUser, on_delete=models.CASCADE, related_name='tep_user')


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='order')
    product_variants = models.OneToOneField(ProductVariant, on_delete=models.CASCADE, related_name='product_variants', blank=True)
    color = models.OneToOneField(Color, on_delete=models.SET_NULL, related_name='colour', blank=True, null=True)
    material = models.OneToOneField(Material, on_delete=models.SET_NULL, related_name='material', blank=True, null=True)
    size = models.OneToOneField(Size, on_delete=models.SET_NULL, related_name='size', blank=True, null=True)
    filter_field = models.ManyToManyField(FilterField, related_name='filter_field', blank=True)
    quantity = models.PositiveIntegerField(default=1)

