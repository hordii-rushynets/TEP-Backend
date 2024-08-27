from django.db import models
from store.models import ProductVariant, Color, Material, Size, FilterField
from tep_user.models import TEPUser


class Cart(models.Model):
    """ Model Cart """
    tep_user = models.OneToOneField(TEPUser, on_delete=models.CASCADE, related_name='tep_user', null=True, blank=True)
    ip_address = models.CharField(max_length=45, unique=True, null=True, blank=True)
    create_data = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        if self.tep_user:
            return f"{self.tep_user.email}"
        return f"Cart for IP {self.ip_address}"


class CartItem(models.Model):
    """Model for ordering a specific product variant"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='order')
    product_variants = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='cart_item',
                                            blank=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, related_name='colour', blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, related_name='material', blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, related_name='size', blank=True, null=True)
    filter_field = models.ManyToManyField(FilterField, related_name='cart_items', blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        if self.cart.tep_user:
            return f"{self.cart.tep_user.email}, {self.product_variants.title}"
        return f"For {self.cart.ip_address}, {self.product_variants.title}"


