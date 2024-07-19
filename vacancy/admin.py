from django.contrib import admin
from .models import Vacancy
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from store.admin import JS, CSS


class VacancyAdmin(TranslationAdmin):
    class Media:
        js = JS
        css = CSS


admin.site.register(Vacancy, VacancyAdmin)
