from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Post, Tag, Complexity, Requirements, Materials, ForChildren


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    exclude = ('title', 'description')


class ComplexityInline(admin.StackedInline):
    model = Complexity
    extra = 1
    exclude = ('title', 'description')


class RequirementsInline(admin.StackedInline):
    model = Requirements
    extra = 1
    exclude = ('title', 'description')


class MaterialsInline(admin.StackedInline):
    model = Materials
    extra = 1
    exclude = ('title', )


class ForChildrenInline(admin.StackedInline):
    model = ForChildren
    extra = 1
    exclude = ('description', 'additional_description')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ['title_uk', 'title_en', 'title_ru', 'slug', 'tags', 'author',
              'meta_description_uk', 'meta_description_en', 'meta_description_ru', 'image']
    inlines = [ComplexityInline, RequirementsInline, MaterialsInline, ForChildrenInline]
    exclude = ('title', 'meta_description')
