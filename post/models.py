from django.db import models

from tep_user.models import TEPUser
from store.models import ProductVariant, Color, Material, Size


class OrderItem(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='order_item')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='order_item', blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='order_item', blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='order_item', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product_variant.title}"


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
    order_item = models.ManyToManyField(OrderItem)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    unique_post_code = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.post_type}: {self.number}"
