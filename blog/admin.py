from django.contrib import admin

from .models import Post, Section, Tag

admin.site.register(Tag)


class SectionInline(admin.TabularInline):
    model = Section
    extra = 1
    fields = ('types', 'title_uk', 'title_en', 'title_ru', 'description_uk', 'description_en', 'description_ru',
              'additional_description_uk', 'additional_description_en', 'additional_description_ru', 'image')
    exclude = ('title', 'description', 'additional_description')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ['title_uk', 'title_en', 'title_ru', 'slug', 'tags', 'author',
              'meta_description_uk', 'meta_description_en', 'meta_description_ru', 'image']
    inlines = [SectionInline]
    exclude = ('title', 'meta_description')
