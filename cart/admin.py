from django.contrib import admin
from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ('tep_user',)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product_variants', 'color', 'material', 'size', )
    filter_horizontal = ('filter_field', )


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
