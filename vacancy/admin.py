from django.contrib import admin
from .models import (Vacancy, ScopeOfWork, TypeOfWork, TypeOfEmployment, Tag, Address, ResponseToVacancy,
                     ResponseToVacancyFile, Cooperation)


class VacancyAdmin(admin.ModelAdmin):
    list_display = ('image', 'title_uk', 'title_en', 'title_ru', 'address', 'description_uk', 'description_en',
                    'description_ru', 'about_company_uk', 'about_company_en', 'creation_time')

    filter_horizontal = ('scope_of_work', 'type_of_work', 'type_of_employment', 'tag')
    exclude = ('title', 'description', 'about_company')


class ScopeOfWorkAdmin(admin.ModelAdmin):
    list_display = ('name_uk', 'name_en', 'name_ru')
    exclude = ('name', )


class TypeOfWorkAdmin(admin.ModelAdmin):
    list_display = ('name_uk', 'name_en', 'name_ru')
    exclude = ('name', )


class TypeOfEmploymentAdmin(admin.ModelAdmin):
    list_display = ('name_uk', 'name_en', 'name_ru')
    exclude = ('name', )


class TagAdmin(admin.ModelAdmin):
    list_display = ('name_uk', 'name_en', 'name_ru')
    exclude = ('name', )


class AddressAdmin(admin.ModelAdmin):
    list_display = ('city_uk', 'region_uk', 'city_en', 'region_en', 'city_ru', 'region_ru')
    exclude = ('city', 'region')


class ResponseToVacancyFileInline(admin.TabularInline):
    model = ResponseToVacancyFile
    extra = 1


class ResponseToVacancyAdmin(admin.ModelAdmin):
    list_display = ('vacancy', 'name', 'email', 'phone')
    search_fields = ('vacancy__title_uk', 'vacancy__title_en', 'vacancy__title_ru')
    inlines = [ResponseToVacancyFileInline]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class CooperationAdmin(admin.ModelAdmin):
    search_fields = ('name', 'phone', 'email', 'topic', 'message')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(ScopeOfWork, ScopeOfWorkAdmin)
admin.site.register(TypeOfWork, TypeOfWorkAdmin)
admin.site.register(TypeOfEmployment, TypeOfEmploymentAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(ResponseToVacancy, ResponseToVacancyAdmin)
admin.site.register(Cooperation, CooperationAdmin)


