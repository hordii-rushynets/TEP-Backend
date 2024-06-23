from modeltranslation.translator import translator, TranslationOptions
from .models import Category, Post, Section


class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'meta_description')


class SectionTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


translator.register(Category, CategoryTranslationOptions)
translator.register(Post, PostTranslationOptions)
translator.register(Section, SectionTranslationOptions)