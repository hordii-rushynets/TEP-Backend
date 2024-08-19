from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Post, Section, Tag


@admin.register(Tag)
class TagAdmin(TranslationAdmin):
    fields = ['slug', 'title_uk', 'title_en', 'title_ru']


class SectionInline(admin.TabularInline):
    model = Section
    extra = 1
    fields = ('types', 'title_uk', 'title_en', 'description_uk', 'description_en', 'additional_description_uk', 'additional_description_en', 'image')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = [('title_uk', 'title_en', 'slug'), 'tags', 'author', 'meta_description_uk', 'meta_description_en', 'image']
    inlines = [SectionInline]
