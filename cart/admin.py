from django.contrib import admin
from .models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user_email')
    search_fields = ('id', 'tep_user__email',)
    filter_horizontal = ('product_variants',)

    def get_user_email(self, obj):
        return obj.tep_user.email

    get_user_email.short_description = 'User Email'
