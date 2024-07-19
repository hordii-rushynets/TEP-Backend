from modeltranslation.translator import translator, TranslationOptions
from .models import (Category, Product, Size, Color, ProductVariant, ProductVariantInfo,
                     Material, Filter, FilterField, DimensionalGrid, DimensionalGridSize)


class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


class DimensionalGridTranslationOptions(TranslationOptions):
    fields = ('title',)


class DimensionalGridSizeTranslationOptions(TranslationOptions):
    fields = ('title', 'size')


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


class FilterTranslationOptions(TranslationOptions):
    fields = ('name',)


class FilterFieldTranslationOptions(TranslationOptions):
    fields = ('value',)


translator.register(Category, CategoryTranslationOptions)
translator.register(Product, ProductTranslationOptions)
translator.register(DimensionalGrid, DimensionalGridTranslationOptions)
translator.register(DimensionalGridSize, DimensionalGridSizeTranslationOptions)
translator.register(Size, SizeTranslationOptions)
translator.register(Color, ColorTranslationOptions)
translator.register(Material, MaterialTranslationOptions)
translator.register(ProductVariant, ProductVariantTranslationOptions)
translator.register(ProductVariantInfo, ProductVariantInfoTranslationOptions)
translator.register(Filter, FilterTranslationOptions)
translator.register(FilterField, FilterFieldTranslationOptions)
