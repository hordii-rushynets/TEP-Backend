from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from tep_user.models import TEPUser, TEPUserSocialNetworks


@admin.register(TEPUserSocialNetworks)
class TEPUserSocialNetworksAdmin(admin.ModelAdmin):
    list_display = ('types', 'user')


@admin.register(TEPUser)
class TEPUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

