from django.db import models

from tep_user.models import TEPUser
from store.models import ProductVariant, Color, Material, Size, FilterField


class OrderItem(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='order_item')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='order_item', blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='order_item', blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='order_item', blank=True, null=True)
    filter_fields = models.ManyToManyField(FilterField, related_name='order_item', blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product_variant.title}"


class Order(models.Model):
    UKRPOST = 'UkrPost'
    NOVAPOST = 'NovaPost'

    POST_TYPE_CHOICES = (
        (UKRPOST, UKRPOST),
        (NOVAPOST, NOVAPOST),
    )

    UPON_RECEIPT = 'UponReceipt'
    BY_CARD = 'ByCard'

    PAYMENT_METHODS = (
        (UPON_RECEIPT, UPON_RECEIPT),
        (BY_CARD, BY_CARD)
    )

    number = models.CharField(max_length=100, blank=True, null=True)
    tep_user = models.ForeignKey(TEPUser, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    ip_address = models.CharField(max_length=45, null=True, blank=True)
    post_type = models.CharField(max_length=100, choices=POST_TYPE_CHOICES)
    order_item = models.ManyToManyField(OrderItem)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    unique_post_code = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=12, default=UPON_RECEIPT, choices=PAYMENT_METHODS)
    paid = models.BooleanField(default=False)
    price = models.FloatField(null=True)
    weight = models.FloatField(null=True)

    def __str__(self):
        if self.tep_user:
            return f"{self.tep_user.email}: {self.number}"
        return f"Order for IP {self.ip_address}: {self.number}"

