from modeltranslation.translator import translator, TranslationOptions
from .models import Category, Product, Size, Color, ProductVariant, ProductVariantInfo, Material


class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


class ProductVariantTranslationOptions(TranslationOptions):
    fields = ('title',)


class SizeTranslationOptions(TranslationOptions):
    fields = ('title',)


class ColorTranslationOptions(TranslationOptions):
    fields = ('title',)


class MaterialTranslationOptions(TranslationOptions):
    fields = ('title',)


class ProductVariantInfoTranslationOptions(TranslationOptions):
    fields = ('material_and_care', 'ecology_and_environment', 'packaging',)


translator.register(Category, CategoryTranslationOptions)
translator.register(Product, ProductTranslationOptions)
translator.register(Size, SizeTranslationOptions)
translator.register(Color, ColorTranslationOptions)
translator.register(Material, MaterialTranslationOptions)
translator.register(ProductVariant, ProductVariantTranslationOptions)
translator.register(ProductVariantInfo, ProductVariantInfoTranslationOptions)