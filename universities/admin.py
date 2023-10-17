from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin
from import_export.fields import Field

from core.my_admin_site import admin_site
from universities.models import University


class UniversityResource(resources.ModelResource):
    name = Field(attribute='name', column_name='Nombre')
    location = Field(attribute='location', column_name='Dirección')

    class Meta:
        model = University
        fields = ('name', 'location', )
        export_order = fields


class UniversityAdmin(ExportMixin, admin.ModelAdmin):
    fields = ['name', 'location', ]
    list_display = ('name', 'location')
    search_fields = ('name', 'location')
    ordering = ('name',)

    resource_class = UniversityResource


admin_site.register(University, UniversityAdmin)
