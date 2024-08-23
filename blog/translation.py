from modeltranslation.translator import translator, TranslationOptions
from .models import Tag, Post, Complexity, Requirements, Materials, ForChildren


class TagTranslationOptions(TranslationOptions):
    fields = ('title',)


class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'meta_description')


class ComplexityTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


class RequirementsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


class MaterialsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


class ForChildrenTranslationOptions(TranslationOptions):
    fields = ('description', 'additional_description')


translator.register(Tag, TagTranslationOptions)
translator.register(Post, PostTranslationOptions)
translator.register(Complexity, ComplexityTranslationOptions)
translator.register(Requirements, RequirementsTranslationOptions)
translator.register(Materials, MaterialsTranslationOptions)
translator.register(ForChildren, ForChildrenTranslationOptions)

