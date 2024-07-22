from django.contrib import admin
from .models import (Product, ProductVariant, Size, Color, Material, ProductVariantInfo, ProductVariantImage,
                     Category, PromoCode, Filter, FilterField, Order, Feedback, DimensionalGrid, DimensionalGridSize,
                     FeedbackImage)
from django.forms import Textarea
from django.db import models
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

JS = (
    'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
    'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
    'modeltranslation/js/tabbed_translation_fields.js',
)
CSS = {
    'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
}


class CategoryAdmin(TranslationAdmin):
    class Media:
        js = JS
        css = CSS


class ColorAdmin(TranslationAdmin):
    class Media:
        js = JS
        css = CSS


class SizeAdmin(TranslationAdmin):
    class Media:
        js = JS
        css = CSS


class MaterialAdmin(TranslationAdmin):
    class Media:
        js = JS
        css = CSS


class ProductVariantImageInline(admin.TabularInline):
    model = ProductVariantImage


class ProductVariantInfoInline(admin.StackedInline):
    model = ProductVariantInfo
    extra = 1


class ProductVariantInline(admin.StackedInline):
    model = ProductVariant


class ProductVariantAdmin(admin.ModelAdmin):
    inlines = [ProductVariantImageInline, ProductVariantInfoInline]


class СustomFilterAdmin(TranslationAdmin):
    class Media:
        js = JS
        css = CSS


class СustomFilterFieldAdmin(TranslationAdmin):
    class Media:
        js = JS
        css = CSS


class DimensionalGridSizeInline(TranslationTabularInline):
    model = DimensionalGridSize


class DimensionalGridAdmin(TranslationAdmin):
    inlines = [DimensionalGridSizeInline]


class FeedbackImageInline(admin.TabularInline):
    model = FeedbackImage
    extra = 1


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['tep_user', 'product', 'text', 'like_number', 'dislike_number', 'evaluation']
    inlines = [FeedbackImageInline]


admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(FeedbackImage)
admin.site.register(Order)
admin.site.register(Category, CategoryAdmin)
admin.site.register(DimensionalGrid, DimensionalGridAdmin)
admin.site.register(Product)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(PromoCode)
admin.site.register(Filter, СustomFilterAdmin)
admin.site.register(FilterField, СustomFilterFieldAdmin)
