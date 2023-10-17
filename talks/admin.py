from django.contrib import admin

from core.my_admin_site import admin_site
from talks.models import *


class DayAdmin(admin.ModelAdmin):
    fields = ('name', 'date', 'active',)
    list_display = ('name', 'date')
    search_fields = ('name', )
    ordering = ('name',)


admin_site.register(Day, DayAdmin)


class RoomAdmin(admin.ModelAdmin):
    fields = ['name', ]
    list_display = ('name', )
    search_fields = ('name', )
    ordering = ('name',)


admin_site.register(Room, RoomAdmin)


class TalkAdmin(admin.ModelAdmin):
    fields = ('title', ('day' , 'room'), ('start_time', 'end_time',), ('logo', 'logo_tag',), ('link_url',
              'is_active', 'is_masterful', ), 'speakers', 'description')
    list_display = ('title', 'day', 'start_time', 'end_time', 'room', 'is_masterful', 'is_active')
    readonly_fields = ('logo_tag', )
    list_filter = ('day', 'room', 'is_masterful', 'is_active')
    search_fields = ('title', )
    ordering = ('title',)
    filter_horizontal = ('speakers', )
    autocomplete_fields = ('day', 'room', )


admin_site.register(Talk, TalkAdmin)


class ActAdmin(admin.ModelAdmin):
    fields = ('title', 'day', ('start_time', 'end_time',), 'link_url', 'is_active',)
    list_display = ('title', 'day', 'start_time', 'end_time', 'is_active', )
    list_filter = ('day', )
    search_fields = ('title', )
    ordering = ('title',)
    autocomplete_fields = ('day', )


admin_site.register(Act, ActAdmin)
