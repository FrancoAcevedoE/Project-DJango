
from import_export.admin import ImportExportActionModelAdmin

from core.my_admin_site import admin_site
from places.models import Country


class UniversityAdmin(ImportExportActionModelAdmin):
    fields = ('id', 'name', 'alpha2', 'alpha3')
    list_display = ('id', 'name', 'alpha2', 'alpha3')
    search_fields = ('name', 'alpha2')
    ordering = ('name',)


admin_site.register(Country, UniversityAdmin)
