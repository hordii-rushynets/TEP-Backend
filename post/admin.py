from django.contrib import admin
from django.contrib import messages

from .models import Order, OrderItem
from .services.factory import get_delivery_service


def delete_orders_and_parcels(modeladmin, request, queryset):
    for order in queryset:
        if order.unique_post_code:
            delivery_service = get_delivery_service(order.post_type)
            deleted = delivery_service.delete_parcel(order.unique_post_code)
            if deleted:
                modeladmin.message_user(request, f"Посилка {order.number} з особистого кабінету.", level=messages.SUCCESS)
            else:
                modeladmin.message_user(request, f"Не вдалося видалити посилку {order.number} з особистого кабінету"
                                                 f"{order.post_type}.", level=messages.ERROR)


delete_orders_and_parcels.short_description = "Видалити вибрані посилки"


class OrderAdmin(admin.ModelAdmin):
    list_display = ('tep_user', 'number', 'post_type', 'unique_post_code', 'created_at')
    list_filter = ('tep_user', 'number', 'post_type', 'unique_post_code', 'created_at')
    search_fields = ('tep_user__email', 'number', 'post_type', 'unique_post_code', 'created_at')

    actions = [delete_orders_and_parcels]

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
