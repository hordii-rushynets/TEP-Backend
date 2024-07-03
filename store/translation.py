from modeltranslation.translator import translator, TranslationOptions
from .models import Category, Product, Size, Color, ProductVariant, ProductVariantInfo, Material, СustomFilterFields


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


class СustomFilterFieldsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


translator.register(Category, CategoryTranslationOptions)
translator.register(Product, ProductTranslationOptions)
translator.register(Size, SizeTranslationOptions)
translator.register(Color, ColorTranslationOptions)
translator.register(Material, MaterialTranslationOptions)
translator.register(ProductVariant, ProductVariantTranslationOptions)
translator.register(ProductVariantInfo, ProductVariantInfoTranslationOptions)
translator.register(СustomFilterFields, СustomFilterFieldsTranslationOptions)