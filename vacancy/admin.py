from django.contrib import admin
from .models import Vacancy, ScopeOfWork, TypeOfWork, TypeOfEmployment, Tag
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


admin.site.register(ScopeOfWork, ScopeOfWorkAdmin)
admin.site.register(TypeOfWork, TypeOfWorkAdmin)
admin.site.register(TypeOfEmployment, TypeOfEmploymentAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Vacancy, VacancyAdmin)
