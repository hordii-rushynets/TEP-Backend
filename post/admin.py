from django.contrib import admin

from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('tep_user', 'number', 'post_type')
    list_filter = ('tep_user', 'number', 'post_type')
    search_fields = ('tep_user__email', 'number', 'post_type')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product_variant', 'color', 'material', 'size', 'quantity')
    list_filter = ('product_variant', 'color', 'material', 'size')
    search_fields = ('product_variant__title', 'color__title', 'material__title', 'size__title')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('product_variant', 'color', 'material', 'size')
        else:
            return ()