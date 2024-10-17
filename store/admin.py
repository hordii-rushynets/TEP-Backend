from django.contrib import admin
from .models import (Product, ProductVariant, Size, Color, Material, ProductVariantInfo, ProductVariantImage,
                     Category, PromoCode, Filter, FilterField, Order, Feedback, DimensionalGrid, DimensionalGridSize,
                     FeedbackImage, ProductImage, InspirationImage, Choice)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['slug', 'title_uk',  'title_en',  'title_ru', 'description_uk', 'description_en', 'description_ru',
                    'image']
    filter_vertical = ['filter']
    exclude = ('title', 'description')


class ColorAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title_uk', 'title_en', 'title_ru', 'hex')
    exclude = ('title', )


class SizeAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title_uk', 'title_en', 'title_ru')
    exclude = ('title', )


class MaterialAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title_uk', 'title_en', 'title_ru')
    exclude = ('title', )


class ProductVariantImageInline(admin.TabularInline):
    model = ProductVariantImage


class ProductVariantInfoInline(admin.StackedInline):
    model = ProductVariantInfo
    extra = 1
    exclude = ('material_and_car', 'ecology_and_environment', 'packaging')


class ProductVariantAdmin(admin.ModelAdmin):
    inlines = [ProductVariantImageInline, ProductVariantInfoInline]
    list_display = ('sku', 'get_product_group_id')
    filter_horizontal = ('sizes', 'colors', 'materials', 'filter_field')
    search_fields = ('sku', 'product__group_id')
    exclude = ('title', )

    def get_product_group_id(self, obj):
        return obj.product.group_id
    get_product_group_id.short_description = 'Group ID'


class FilterFieldInline(admin.TabularInline):
    model = FilterField
    extra = 1


class FilterAdmin(admin.ModelAdmin):
    inlines = [FilterFieldInline]
    list_display = ('name_uk', 'name_en', 'name_ru')
    exclude = ('name', )


class FilterFieldAdmin(admin.ModelAdmin):
    list_display = ('filter', 'value_uk', 'value_en', 'value_ru')
    exclude = ('value', )


class DimensionalGridSizeInline(admin.TabularInline):
    model = DimensionalGridSize
    extra = 1
    list_display = ('dimensional_grid', 'title_uk', 'title_en', 'title_ru', 'size_uk', 'size_en', 'size_ru')
    exclude = ('title', 'size')


class DimensionalGridAdmin(admin.ModelAdmin):
    inlines = [DimensionalGridSizeInline]
    search_fields = ('title_uk', 'title_en', 'title_ru', 'product__title_uk',
                     'product__title_en', 'product__title_ru', 'product__slug')
    list_filter = ('title_uk', 'product__slug')
    exclude = ('title', )


class FeedbackImageInline(admin.TabularInline):
    model = FeedbackImage
    extra = 1


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['tep_user', 'product', 'text', 'like_number', 'dislike_number', 'evaluation']
    inlines = [FeedbackImageInline]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

    verbose_name = "Product photo in interior"
    verbose_name_plural = "Photos of products in the interior"


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'description', 'category', 'group_id']
    filter_horizontal = ['dimensional_grid']
    inlines = [ProductImageInline]
    exclude = ('title', 'description', 'dimensional_grid_description')
    search_fields = ['slug', 'description', 'group_id']


class ChoiceAdmin(admin.ModelAdmin):
    filter_horizontal = ['filter_fields']
    search_fields = ['filter__name', 'filter_fields__value']


admin.site.register(Order)
admin.site.register(Category, CategoryAdmin)
admin.site.register(DimensionalGrid, DimensionalGridAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(PromoCode)
admin.site.register(Filter, FilterAdmin)
admin.site.register(FilterField, FilterFieldAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(FeedbackImage)
admin.site.register(InspirationImage)
admin.site.register(Choice, ChoiceAdmin)
