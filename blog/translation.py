from modeltranslation.translator import translator, TranslationOptions
from .models import Tag, Post, Section


class TagTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'meta_description')


class SectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'additional_description')


translator.register(Tag, TagTranslationOptions)
translator.register(Post, PostTranslationOptions)
translator.register(Section, SectionTranslationOptions)