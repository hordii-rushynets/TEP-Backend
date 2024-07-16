from django.db import models
from store.models import ProductVariant, Color, Material, Size, FilterField
from tep_user.models import TEPUser


class Cart(models.Model):
    """
    Model for storing a user's shopping cart with the products they have added to it.

    Fields:
    - tep_user: One-to-One relationship with TEPUser model, representing the user associated with the cart.
    """
    tep_user = models.OneToOneField(TEPUser, on_delete=models.CASCADE, related_name='tep_user')


class CartItem(models.Model):
    """
    Model for ordering a specific product variant.

    Fields:
    - cart: ForeignKey to Cart model, representing the cart to which the item belongs.
    - product_variants: One-to-One relationship with ProductVariant model, representing the selected product variant.
    - color: One-to-One relationship with Color model, representing the selected color (nullable).
    - material: One-to-One relationship with Material model, representing the selected material (nullable).
    - size: One-to-One relationship with Size model, representing the selected size (nullable).
    - filter_field: Many-to-Many relationship with FilterField model, representing additional filter fields associated with the product.
    - quantity: Positive integer field representing the quantity of the product variant ordered.

    """

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='order')
    product_variants = models.OneToOneField(ProductVariant, on_delete=models.CASCADE, related_name='product_variants', blank=True)
    color = models.OneToOneField(Color, on_delete=models.SET_NULL, related_name='colour', blank=True, null=True)
    material = models.OneToOneField(Material, on_delete=models.SET_NULL, related_name='material', blank=True, null=True)
    size = models.OneToOneField(Size, on_delete=models.SET_NULL, related_name='size', blank=True, null=True)
    filter_field = models.ManyToManyField(FilterField, related_name='filter_field', blank=True)
    quantity = models.PositiveIntegerField(default=1)

