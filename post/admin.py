from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderNumberAdmin(admin.ModelAdmin):
    list_display = ('tep_user', 'number', 'post_type')
    list_filter = ('tep_user', 'number', 'post_type')
    search_fields = ('tep_user__email', 'number', 'post_type')