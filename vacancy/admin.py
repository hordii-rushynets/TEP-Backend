from django.contrib import admin
from .models import Vacancy, ScopeOfWork, TypeOfWork, TypeOfEmployment, Tag, Address, CooperationOffer
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from store.admin import JS, CSS


class VacancyAdmin(TranslationAdmin):
    class Media:
        js = JS
        css = CSS


class ScopeOfWorkAdmin(TranslationAdmin):
    class Media:
        js = JS
        css = CSS


class TypeOfWorkAdmin(TranslationAdmin):
    class Media:
        js = JS
        css = CSS


class TypeOfEmploymentAdmin(TranslationAdmin):
    class Media:
        js = JS
        css = CSS


class TagAdmin(TranslationAdmin):
    class Media:
        js = JS
        css = CSS


class AddressAdmin(TranslationAdmin):
    class Media:
        js = JS
        css = CSS


class CooperationOfferAdmin(admin.ModelAdmin):
    list_display = ('vacancy', 'name', 'email', 'phone')
    search_fields = ('vacancy__title_uk', 'vacancy__title_en', 'vacancy__title_ru')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(ScopeOfWork, ScopeOfWorkAdmin)
admin.site.register(TypeOfWork, TypeOfWorkAdmin)
admin.site.register(TypeOfEmployment, TypeOfEmploymentAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(CooperationOffer, CooperationOfferAdmin)


