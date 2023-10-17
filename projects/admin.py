from django import forms
from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin
from import_export.fields import Field

from core.my_admin_site import admin_site
from projects.models import *


class ProyectoResource(resources.ModelResource):
    title = Field(attribute='title', column_name='Título')
    main_theme = Field(attribute='main_theme', column_name='Eje Temático')
    author = Field(attribute='author', column_name='Responsable')
    author_email = Field(attribute='author_email', column_name='Responsable email')
    university = Field(attribute='author__university__name', column_name='Universidad')
    status = Field(attribute='get_status_display', column_name='Estado')
    commission = Field(attribute='commission', column_name='Mesa')
    commission_date_time = Field(attribute='commission_date_time', column_name='Fecha Mesa')
    commission_youtube_url = Field(attribute='commission_youtube_url', column_name='Mesa YouTube')
    commission_zoom_url = Field(attribute='commission_zoom_url', column_name='Mesa Zoom')
    commission_moderator = Field(attribute='commission_moderator', column_name='Moderador Mesa')
    authors = Field(attribute='authors', column_name='Autores')

    class Meta:
        model = Project
        fields = ('title', 'main_theme', 'author', 'author_email', 'authors', 'university', 'status',
                  'commission_date_time', 'commission', 'commission_youtube_url', 'commission_zoom_url',
                  'commission_moderator', )
        export_order = fields

    def dehydrate_authors(self, project):
        authors = project.authors.values_list('first_name', 'last_name', 'document_number',)
        return ';'.join(map(lambda x: ' ' + "%s %s - %s" % (x[0], x[1], x[2]), authors))


class MainThemeForm(forms.ModelForm):

    A1 = 'Lucha contra el Covid-19'

    B1 = 'Prácticas sociales y educativas en territorio'
    B2 = 'Prácticas aprendizaje-servicio'
    B3 = 'Trayectos de formación integral'
    B4 = 'Voluntariados'
    B5 = 'Cátedras específicas'
    B6 = 'Iniciativas novedosas en la curricularización de la extensión universitaria'

    C1 = 'Aportes a políticas sociales en territorios diversos'
    C2 = 'Protecciones sociales de grupos vulnerados'
    C3 = 'Salud comunitaria y salud ambiental'
    C4 = 'Educación de calidad, inclusiva y equitativa'
    C5 = 'Economía social e inclusión socio productiva'
    C6 = 'Procesos barriales, territoriales y comunitarios'
    C7 = 'Arte y cultura popular'
    C8 = 'Promoción de la igualdad entre los géneros'
    C9 = 'Transversalización de la perspectiva de discapacidad'
    C10 = 'Pueblos originarios; Innovación ciudadana y emprendedores sociales'

    D1 = 'Jerarquización e institucionalización de la extensión'
    D2 = 'Aportes a la definición de indicadores para la evaluación y sistematización de la extensión'
    D3 = 'Reconocimiento de la labor extensionista en la carrera docente'
    D4 = 'Trabajadores no docentes y extensión'
    D5 = 'Propuestas de formación en extensión'
    D6 = 'Experiencias metodológicas de plataformas territoriales'
    D7 = 'Comunicación, difusión y visibilización de la extensión'
    D8 = 'Estrategias y dispositivos innovadores en la gestión de la extensión'

    MAIN_THEME_CHOICES = (
        (Commission.THEME_A, ((A1, A1),)),
        (Commission.THEME_B, ((B1, B1), (B2, B2), (B3, B3), (B4, B4), (B5, B5), (B6, B6),)),
        (Commission.THEME_C, ((C1, C1), (C2, C2), (C3, C3), (C4, C4), (C5, C5), (C6, C6), (C7, C7), (C8, C8), (C9, C9), (C10, C10),)),
        (Commission.THEME_D, ((D1, D1), (D2, D2), (D3, D3), (D4, D4), (D5, D5), (D6, D6), (D7, D7), (D8, D8),)),
    )

    main_theme = forms.ChoiceField(choices=MAIN_THEME_CHOICES, label='EJE TEMÁTICO')


class CommissionResource(resources.ModelResource):
    name = Field(attribute='name', column_name='Nombre')
    date_time_localize = Field(attribute='date_time_localize', column_name='Fecha y Hora')
    moderator = Field(attribute='moderator', column_name='Moderador')
    youtube_url = Field(attribute='youtube_url', column_name='Link de YouTube')
    zoom_url = Field(attribute='zoom_url', column_name='Link de Zoom')
    amount_of_participants = Field(attribute='amount_of_participants', column_name='cant. de participantes')
    theme = Field(attribute='get_theme_display', column_name='Eje')
    technical_operator = Field(attribute='technical_operator', column_name='Asistente de mesa')
    observation = Field(attribute='observation', column_name='Observación')

    class Meta:
        model = Commission
        fields = ('name', 'date_time_localize', 'moderator', 'youtube_url', 'zoom_url', 'amount_of_participants',
                  'theme', 'technical_operator', 'observation', )
        export_order = fields


class CommissionAdmin(ExportMixin, admin.ModelAdmin):
    fields = ('name', 'date_time', ('theme', 'amount_of_participants',), ('moderator', 'technical_operator',),
              ('youtube_url', 'zoom_url',), 'observation')
    list_display = ('name', 'date_time', 'youtube_url', 'zoom_url', 'short_observation')
    search_fields = ('name', 'theme', )
    ordering = ('-name', )
    list_filter = ('theme', )

    resource_class = CommissionResource

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "moderator" or db_field.name == "technical_operator":
            kwargs["queryset"] = Person.objects.filter(user_type=Person.COLLABORATOR, is_active=True)
            #db = kwargs.get('using')
            #kwargs['widget'] = AutocompleteSelect(db_field.remote_field, self.admin_site, using=db)

        return super(CommissionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin_site.register(Commission, CommissionAdmin)


class ConferenceResource(resources.ModelResource):
    name = Field(attribute='name', column_name='Nombre')
    date_time_localize = Field(attribute='date_time_localize', column_name='Fecha y Hora')
    youtube_url = Field(attribute='youtube_url', column_name='Link de YouTube')
    zoom_url = Field(attribute='zoom_url', column_name='Link de Zoom')
    observation = Field(attribute='observation', column_name='Observación')

    class Meta:
        model = Commission
        fields = ('name', 'date_time_localize', 'youtube_url', 'zoom_url', 'observation', )
        export_order = fields


class ConferenceAdmin(ExportMixin, admin.ModelAdmin):
    fields = ('name', 'date_time', ('youtube_url', 'zoom_url',), 'observation')
    list_display = ('name', 'date_time', 'youtube_url', 'zoom_url', 'short_observation')
    search_fields = ('name',)
    ordering = ('-name', )

    resource_class = ConferenceResource


admin_site.register(Conference, ConferenceAdmin)


class WorkshopResource(resources.ModelResource):
    title = Field(attribute='title', column_name='Título')
    date_time_localize = Field(attribute='date_time_localize', column_name='Fecha y Hora')
    technical_operator = Field(attribute='technical_operator', column_name='Operador Técnico')
    responsable = Field(attribute='responsable', column_name='Responsable')
    youtube_url = Field(attribute='youtube_url', column_name='Link de YouTube')
    zoom_url = Field(attribute='zoom_url', column_name='Link de Zoom')
    observation = Field(attribute='observation', column_name='Observación')

    class Meta:
        model = Workshop
        fields = ('title', 'date_time_localize', 'responsable', 'technical_operator', 'youtube_url', 'zoom_url',
                  'observation',)
        export_order = fields


class WorkshopAdmin(ExportMixin, admin.ModelAdmin):
    fields = ('title', 'responsable', 'date_time', ('youtube_url', 'zoom_url',), 'observation')
    list_display = ('title', 'responsable', 'date_time', 'youtube_url', 'zoom_url', 'short_observation')

    resource_class = WorkshopResource


admin_site.register(Workshop, WorkshopAdmin)


class AudienceAdmin(admin.ModelAdmin):
    fields = ('title', 'date_time', ('youtube_url', 'zoom_url',), 'commission', 'observation')
    list_display = ('title', 'date_time', 'youtube_url', 'zoom_url', 'short_observation')
    list_filter = ('commission', )
    autocomplete_fields = ('commission',)


admin_site.register(Audience, AudienceAdmin)


class AuthorInline(admin.TabularInline):
    model = ProjectAuthor
    extra = 1
    fields = ('line_number', 'first_name', 'last_name', 'document_type', 'document_number', 'email', 'university')
    autocomplete_fields = ('university',)
    readonly_fields = ('line_number', )
    show_change_link = False

    line_numbering = 0

    def line_number(self, obj):
        self.line_numbering += 1
        return self.line_numbering

    line_number.short_description = '#'


class NoteProjectInline(admin.TabularInline):
    model = NoteProject
    fields = ('line_number', 'note', 'date',)
    readonly_fields = ('line_number', 'date')
    show_change_link = False
    extra = 0

    line_numbering = 0

    def line_number(self, obj):
        self.line_numbering += 1
        return self.line_numbering

    line_number.short_description = '#'


class ProjectAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('title', 'main_theme', 'author',)
    readonly_fields = ('image_tag', 'status', 'commission_description')
    readonly_fields_admin = ('image_tag', 'theme', 'commission_description', )
    list_filter = ('commission', 'main_theme', 'status',)
    search_fields = ('title', 'author__first_name', 'author__last_name')
    inlines_news = (AuthorInline,)
    inlines = (AuthorInline, NoteProjectInline,)
    ordering = ('title', 'main_theme',)
    autocomplete_fields = ('author',)
    form = MainThemeForm
    actions = ()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user
        if db_field.name == "author" and not user.is_superuser or not (user.user_type == Person.ORGANIZER):
            kwargs["initial"] = user.pk
        return super(ProjectAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(ProjectAdmin, self).get_queryset(request)
        user = request.user
        user_type = user.user_type
        if not user.is_superuser and \
                (user_type == Person.ASSISTANT or user_type == Person.SPEAKER or user_type == Person.STUDENT):
            return qs.filter(author=user)
        else:
            return qs

    def get_list_filter(self, request):
        user = request.user
        user_type = user.user_type
        if not user.is_superuser and \
                (user_type == Person.ASSISTANT or user_type == Person.SPEAKER or user_type == Person.STUDENT):
            return ()
        else:
            return super(ProjectAdmin, self).get_list_filter(request)

    def has_export_permission(self, request):
        user = request.user
        user_type = user.user_type
        if not user.is_superuser and \
                (user_type == Person.ASSISTANT or user_type == Person.SPEAKER or user_type == Person.STUDENT):
            return False
        else:
            return super(ProjectAdmin, self).has_export_permission(request)

    def get_search_fields(self, request):
        user = request.user
        user_type = user.user_type
        if not user.is_superuser and \
                (user_type == Person.ASSISTANT or user_type == Person.SPEAKER):
            return ()
        else:
            return super(ProjectAdmin, self).get_search_fields(request)

    def get_readonly_fields(self, request, obj=None):
        user = request.user
        user_type = user.user_type
        if not user.is_superuser and \
                (user_type == Person.ASSISTANT or user_type == Person.SPEAKER):
            return super(ProjectAdmin, self).get_readonly_fields(request, obj)
        else:
            return self.readonly_fields_admin

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in filter(lambda obj: isinstance(obj, NoteProject), instances):
            if instance.__dict__.get('author', None) is None:
                instance.author = request.user
                instance.save()
        formset.save_m2m()
        super(ProjectAdmin, self).save_formset(request, form, formset, change)

    def get_inlines(self, request, obj):
        inlines = super(ProjectAdmin, self).get_inlines(request, obj)
        user = request.user
        user_type = user.user_type
        if not user.is_superuser and \
                (user_type == Person.ASSISTANT or user_type == Person.SPEAKER or user_type == Person.COLLABORATOR):
            if obj is None or not (obj.status is Project.REQUEST_FOR_CHANGES):
                return self.inlines_news
            else:
                return inlines
        else:
            return inlines

    def save_model(self, request, obj, form, change):
        user = request.user
        user_type = user.user_type
        if not user.is_superuser and \
                (user_type == Person.ASSISTANT or user_type == Person.SPEAKER):
            if 'abstract' in form.changed_data or \
                    'image' in form.changed_data or \
                    'document' in form.changed_data or \
                    'video' in form.changed_data:
                obj.status = Project.PENDING

        main_theme = obj.main_theme
        if main_theme == MainThemeForm.A1:
            obj.theme = '1'
        elif main_theme == MainThemeForm.B1 or main_theme == MainThemeForm.B2 or main_theme == MainThemeForm.B3 or main_theme == MainThemeForm.B4 or main_theme == MainThemeForm.B5 or main_theme == MainThemeForm.B6:
            obj.theme = '2'
        elif main_theme == MainThemeForm.D1 or main_theme == MainThemeForm.D2 or main_theme == MainThemeForm.D3 or main_theme == MainThemeForm.D4 or main_theme == MainThemeForm.D5 or main_theme == MainThemeForm.D6 or main_theme == MainThemeForm.D7 or main_theme == MainThemeForm.D8:
            obj.theme = '4'
        else:
            obj.theme = '3'

        super(ProjectAdmin, self).save_model(request, obj, form, change)


admin_site.disable_action('delete_selected')


class PresentationInline(AuthorInline):
    max_num = 5
    verbose_name_plural = "AUTORES (Máximo 5)"


class PresentationResource(ProyectoResource):
    document = Field(attribute='document_resource_url', column_name='Documento')

    class Meta:
        model = Presentation
        fields = ('title', 'main_theme', 'author', 'author_email', 'authors', 'university', 'document', 'status',
                  'commission_date_time', 'commission', 'commission_youtube_url', 'commission_zoom_url',
                  'commission_moderator',)
        export_order = fields


class PresentationAdmin(ProjectAdmin):
    fields = ('title', ('main_theme', 'commission',), 'commission_description', 'tags', 'author', 'status', 'document',
              'abstract',)
    list_display = ('title', 'main_theme', 'commission', 'author', 'document', 'status', 'project_actions')
    inlines_news = (PresentationInline,)
    readonly_fields = ('commission_description', )
    inlines = (PresentationInline, NoteProjectInline,)

    resource_class = PresentationResource

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Mis Ponencias'}
        return super(PresentationAdmin, self).changelist_view(request, extra_context=extra_context)


admin_site.register(Presentation, PresentationAdmin)


class VideoPosterResource(ProyectoResource):
    youtube_url = Field(attribute='youtube_url', column_name='Link de YouTube')

    class Meta:
        model = VideoPoster
        fields = ('title', 'main_theme', 'author', 'author_email', 'authors', 'university', 'youtube_url', 'status',
                  'commission_date_time', 'commission', 'commission_youtube_url', 'commission_zoom_url',
                  'commission_moderator',)
        export_order = fields


class VideoPosterAdmin(ProjectAdmin):
    fields = ('title', ('main_theme', 'commission'), 'commission_description', 'tags', 'author', 'status', 'video',
              'youtube_url', 'abstract',)
    readonly_fields = ('commission_description', )
    list_display = ('title', 'main_theme', 'commission', 'author', 'youtube_url', 'status', 'project_actions')

    resource_class = VideoPosterResource

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Mis Videos'}
        return super(VideoPosterAdmin, self).changelist_view(request, extra_context=extra_context)

    def get_form(self, request, obj=None, change=False, **kwargs):
        help_texts = {'abstract': 'El resumen debe contener: Responsable del proyecto o actividad, mail, tel; si el proyecto tuviese redes sociales mencionarlas; Universidad y unidad académica o departamento; Resto del equipo extensionista; Título; Objetivos; Actividades desarrolladas; Instituciones y organizaciones involucradas; En el caso de tener resultados, mencionar debilidades y fortalezas; Conclusiones y proyecciones'}
        kwargs.update({'help_texts': help_texts})
        return super(VideoPosterAdmin, self).get_form(request, obj, **kwargs)


admin_site.register(VideoPoster, VideoPosterAdmin)


class PosterResource(ProyectoResource):
    image = Field(attribute='image_resource_url', column_name='Imagen')

    class Meta:
        model = Presentation
        fields = ('title', 'main_theme', 'author', 'author_email', 'authors', 'university', 'image', 'status',
                  'commission_date_time', 'commission', 'commission_youtube_url', 'commission_zoom_url',
                  'commission_moderator',)
        export_order = fields


class PosterAdmin(ProjectAdmin):
    fields = ('title', ('main_theme', 'commission',), 'commission_description', 'tags', 'author', 'status',
              ('image', 'image_tag',), 'abstract', )
    list_display = ('title', 'main_theme', 'commission', 'author', 'image_tag', 'status', 'project_actions')

    resource_class = PosterResource

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Mis Posters'}
        return super(PosterAdmin, self).changelist_view(request, extra_context=extra_context)

    def get_form(self, request, obj=None, change=False, **kwargs):
        help_texts = {'abstract': 'El resumen debe contener: Responsable del proyecto o actividad, mail, tel; si el proyecto tuviese redes sociales mencionarlas; Universidad y unidad académica o departamento; Resto del equipo extensionista; Título; Objetivos; Actividades desarrolladas; Instituciones y organizaciones involucradas; En el caso de tener resultados, mencionar debilidades y fortalezas; Conclusiones y proyecciones'}
        kwargs.update({'help_texts': help_texts})
        return super(PosterAdmin, self).get_form(request, obj, **kwargs)


admin_site.register(Poster, PosterAdmin)
