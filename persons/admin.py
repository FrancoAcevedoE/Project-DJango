from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import Q
from import_export import resources
from import_export.admin import ExportMixin
from import_export.fields import Field

from core.my_admin_site import admin_site
from .models import *


class PersonResource(resources.ModelResource):
    #university = fields.Field(column_name='university', attribute='university', widget=ForeignKeyWidget(University, 'name'))
    university = Field(attribute='university__name', column_name='Universidad')
    email = Field(attribute='email', column_name='Correo')
    first_name = Field(attribute='first_name', column_name='Nombre')
    last_name = Field(attribute='last_name', column_name='Apellido')
    document_number = Field(attribute='document_number', column_name='Documento')
    country = Field(attribute='country__name', column_name='Pais')
    date_joined = Field(attribute='date_joined', column_name='Fecha creación')
    user_type = Field(attribute='get_user_type_display', column_name='Tipo')
    relation = Field(attribute='get_relation_display', column_name='Relación')
    affiliation = Field(attribute='affiliation', column_name='Filiación')

    def before_import_row(self, row, row_number=None, **kwargs):
        university_name = row['university']
        university, created = University.objects.get_or_create(name=university_name)
        university_id = university.pk
        row['university'] = university_id

    class Meta:
        model = Person
        fields = ('email', 'first_name', 'last_name', 'document_number', 'university', 'country', 'user_type',
                  'relation', 'affiliation', 'date_joined')
        export_order = fields
        import_id_fields = ('email', )


class PersonAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'document_number', 'email', 'user_type', 'country', 'this_payment',
                    'profile_picture_short_tag', )
    search_fields = ('document_number', 'first_name', 'last_name', 'email',)
    ordering = ('last_name', 'first_name', )
    fields = (('email', 'document_number', ), ('last_name', 'first_name',),
              ('profile_picture_medium_tag', 'profile_picture',),
              ('country', 'university', 'relation', 'affiliation', ), ('user_type', 'is_active',), 'password',
              'this_payment', 'description')
    user_profile_fields = (('last_name', 'first_name',), ('profile_picture', 'profile_picture_medium_tag',),
                           ('country', 'university',), ('relation', 'affiliation',), 'document_number',)

    extra_fields = ('username', ('email', 'document_number', ), ('last_name', 'first_name',),
                    ('profile_picture_medium_tag', 'profile_picture',),
                    ('country', 'university', 'relation', 'affiliation', ), ('is_active', 'is_superuser', 'is_staff',),
                    'user_type', 'password', 'this_payment', 'description')

    readonly_fields = ('profile_picture_medium_tag', )
    readonly_fields_speaker = ('profile_picture_medium_tag', 'user_type')
    list_filter = ('is_active', 'this_payment', 'user_type', 'university', 'country', 'relation', )
    extra_list_filter = ('is_active', 'is_staff', 'this_payment', 'user_type', 'university', 'country', 'relation',)
    autocomplete_fields = ('country', 'university', )

    resource_class = PersonResource

    def get_queryset(self, request):
        qs = super(PersonAdmin, self).get_queryset(request)
        user = request.user

        if not user.is_superuser:
            user_type = user.user_type
            if user_type == Person.COLLABORATOR or user_type == Person.EXTERNAL_COLLABORATOR:
                return qs.filter(Q(user_type=Person.ASSISTANT, is_active=True) |
                                 Q(user_type=Person.SPEAKER, is_active=True) |
                                 Q(pk=user.pk))

            elif user_type == Person.ORGANIZER:
                return qs.exclude(user_type=Person.ORGANIZER)

            else:
                return qs.filter(pk=user.pk)

        return qs

    def get_list_filter(self, request):
        user = request.user
        user_type = user.user_type
        if not user.is_superuser:

            if user_type == Person.SPEAKER or user_type == Person.ASSISTANT:
                return ()
            else:
                return super(PersonAdmin, self).get_list_filter(request)
        else:
            return self.extra_list_filter

    def get_fields(self, request, obj=None):
        user = request.user
        if not user.is_superuser:
            user_type = user.user_type
            if user_type == Person.SPEAKER or user_type == Person.ASSISTANT or user_type == Person.COLLABORATOR:
                return self.user_profile_fields

            else:
                return self.fields

        else:
            return self.extra_fields

    def get_readonly_fields(self, request, obj=None):
        user = request.user
        if not user.is_superuser:
            user_type = user.user_type
            if user_type == Person.SPEAKER or user_type == Person.ASSISTANT or user_type == Person.COLLABORATOR:
                return self.readonly_fields_speaker

        return super(PersonAdmin, self).get_readonly_fields(request, obj)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        user = request.user

        if db_field.name == 'status' and not user.is_superuser:
            user_type = user.user_type
            if user_type == Person.COLLABORATOR or user_type == Person.EXTERNAL_COLLABORATOR:
                kwargs["choices"] = Person.USER_TYPE_CHOICES_COLLABORATOR

            elif user_type == Person.ORGANIZER:
                kwargs["choices"] = Person.USER_TYPE_CHOICES_ORGANIZER

        return db_field.formfield(**kwargs)

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(obj.password)
        obj.save()

        if 'user_type' in form.changed_data:
            obj.groups.clear()
            obj.save()
            admin_group_user = Group.objects.get(name=obj.user_type)
            admin_group_user.user_set.add(obj.pk)
            admin_group_user.save()

    def delete_model(self, request, obj):
        user = request.user
        if not user.is_superuser:
            obj.is_active = False
            obj.save()
        else:
            obj.delete()


admin_site.register(Person, PersonAdmin)
admin_site.register(Group)
