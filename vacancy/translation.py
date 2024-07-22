from modeltranslation.translator import translator, TranslationOptions
from .models import Vacancy, Tag, TypeOfWork, TypeOfEmployment, ScopeOfWork


class VacancyTranslationOptions(TranslationOptions):
    fields = ('title', 'city', 'region', 'description', 'about_company')


class TagTranslationOptions(TranslationOptions):
    fields = ('name',)


class TypeOfWorkTranslationOptions(TranslationOptions):
    fields = ('name',)


class TypeOfEmploymentTranslationOptions(TranslationOptions):
    fields = ('name',)


class ScopeOfWorkTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Vacancy, VacancyTranslationOptions)
translator.register(Tag, TagTranslationOptions)
translator.register(TypeOfWork, TypeOfWorkTranslationOptions)
translator.register(TypeOfEmployment, TypeOfEmploymentTranslationOptions)
translator.register(ScopeOfWork, ScopeOfWorkTranslationOptions)
