from django.contrib import admin
from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    """
    Admin configuration for Cart model.

    Attributes:
    - list_display: Tuple of fields to display in the admin list view of Cart instances.
    """

    list_display = ('tep_user',)


class CartItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for CartItem model.

    Attributes:
    - list_display: Tuple of fields to display in the admin list view of CartItem instances.
    - filter_horizontal: Tuple of fields to display as horizontal filter widgets in the admin detail view of CartItem instances.
    """

    list_display = ('cart', 'product_variants', 'color', 'material', 'size', )
    filter_horizontal = ('filter_field', )


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
