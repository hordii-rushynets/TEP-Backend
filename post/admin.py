from django.contrib import admin
from .models import OrderNumber


@admin.register(OrderNumber)
class OrderNumberAdmin(admin.ModelAdmin):
    list_display = ('tep_user', 'number', 'post_type')
    list_filter = ('tep_user', 'number', 'post_type')
    search_fields = ('tep_user', 'number', 'post_type')