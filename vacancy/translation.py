from modeltranslation.translator import translator, TranslationOptions
from .models import Vacancy, Tag, TypeOfWork, TypeOfEmployment, ScopeOfWork, Address


class VacancyTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'about_company')


class TagTranslationOptions(TranslationOptions):
    fields = ('name',)


class TypeOfWorkTranslationOptions(TranslationOptions):
    fields = ('name',)


class TypeOfEmploymentTranslationOptions(TranslationOptions):
    fields = ('name',)


class ScopeOfWorkTranslationOptions(TranslationOptions):
    fields = ('name',)


class AddressTranslationOptions(TranslationOptions):
    fields = ('region', 'city')


translator.register(Vacancy, VacancyTranslationOptions)
translator.register(Tag, TagTranslationOptions)
translator.register(TypeOfWork, TypeOfWorkTranslationOptions)
translator.register(TypeOfEmployment, TypeOfEmploymentTranslationOptions)
translator.register(ScopeOfWork, ScopeOfWorkTranslationOptions)
translator.register(Address, AddressTranslationOptions)
