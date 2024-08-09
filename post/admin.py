from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError

from .models import Order, OrderItem

from .services.nova_poshta_delivery_service import NovaPoshtaService


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('tep_user', 'number', 'post_type')
    list_filter = ('tep_user', 'number', 'post_type')
    search_fields = ('tep_user__email', 'number', 'post_type')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def delete_selected(self, request, queryset):
        for order in queryset:
            tracking_number = order.number
            try:
                result = NovaPoshtaService().delete_parcel(tracking_number)
                messages.success(request, f"Order {order.number}: {result}")
            except ValidationError as e:
                messages.error(request, f"Order {order.number}: {e}")

    actions = [delete_selected]


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