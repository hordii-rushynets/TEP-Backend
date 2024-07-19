from modeltranslation.translator import translator, TranslationOptions
from .models import Vacancy


class VacancyTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'address', 'employment_type', 'about_company')


translator.register(Vacancy, VacancyTranslationOptions)
