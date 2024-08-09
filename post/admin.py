from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('tep_user', 'number', 'post_type')
    list_filter = ('tep_user', 'number', 'post_type')
    search_fields = ('tep_user__email', 'number', 'post_type')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
