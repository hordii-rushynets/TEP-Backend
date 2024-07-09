from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tep_user.models import TEPUser, Cart


@admin.register(TEPUser)
class TEPUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name','is_active')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user_email')
    search_fields = ('id', 'tep_user__email',)
    filter_horizontal = ('product_variants',)

    def get_user_email(self, obj):
        return obj.tep_user.email

    get_user_email.short_description = 'User Email'
