from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.template.defaultfilters import truncatechars
from django.templatetags.l10n import localize
from django.urls import reverse
from django.utils.html import format_html
from django.utils.timezone import now, localtime
from django.utils.translation import gettext_lazy as _
from django_upload_path.upload_path import auto_cleaned_path_stripped_uuid4
from taggit.managers import TaggableManager

from persons.models import Person
from universities.models import University
from core.utils.youtube import youtube_url_to_embed


class ExtensionValidator(RegexValidator):
    def __init__(self, extensions, message=None):
        if not hasattr(extensions, '__iter__'):
            extensions = [extensions]
        regex = '\.(%s)$' % '|'.join(extensions)
        if message is None:
            message = 'File type not supported. Accepted types are: %s.' % ', '.join(extensions)
        super(ExtensionValidator, self).__init__(regex, message)

    def __call__(self, value):
        super(ExtensionValidator, self).__call__(value.name)


def validate_pdf_file_extension(value):
    if value.file.content_type != 'application/pdf':
        raise ValidationError(u'Error message')


class Thematic(models.Model):
    name = models.CharField('nombre', max_length=200)
    image = models.ImageField(_('imágen'), upload_to=auto_cleaned_path_stripped_uuid4, null=True, blank=True)

    def logo_tag(self):
        if self.image:
            url_image = self.image.url
            return format_html("""<img src='{}' width='40'"/>""", url_image)
        return "-"
    logo_tag.short_description = _('imagen previa')
    logo_tag.allow_tags = True

    class Meta:
        verbose_name = 'temática'
        verbose_name_plural = 'temáticas'

    def __str__(self):
        return self.name


class Commission(models.Model):
    name = models.CharField('NOMBRE', max_length=200)
    date_time = models.DateTimeField(verbose_name="FECHA Y HORA", default=now, blank=True, null=True)
    youtube_url = models.URLField('Link de YouTube', null=True, blank=True)
    zoom_url = models.URLField('Link de Zoom', null=True, blank=True)
    moderator = models.CharField("moderador", max_length=200, blank=False, null=True)
    THEME_A = 'Políticas públicas y Universidad: el rol de la extensión universitaria en el acompañamiento y asistencia en la pandemia por Covid-19'
    THEME_B = 'Enfoques teóricos, metodológicos y prácticos para la curricularización de la extensión'
    THEME_C = 'Praxis extensionistas y construcción colectiva del conocimiento'
    THEME_D = 'Estrategias de gestión integral para el abordaje institucional de la extensión'
    THEME_CHOICES = (
        ('1', THEME_A),
        ('2', THEME_B),
        ('3', THEME_C),
        ('4', THEME_D),
    )
    amount_of_participants = models.IntegerField('cant. de participantes', null=True, blank=True)
    theme = models.CharField('eje', max_length=2, choices=THEME_CHOICES, null=True, blank=True)
    technical_operator = models.CharField("asistente de mesa", max_length=200, blank=False, null=True)
    observation = models.TextField(_("observación"), blank=True)

    def short_observation(self):
        return truncatechars(self.observation, 300)
    short_observation.short_description = _('observación')
    short_observation.allow_tags = True

    @property
    def date_time_localize(self):
        return localize(localtime(self.date_time))

    @property
    def youtube_url_embed(self):
        return youtube_url_to_embed(self.youtube_url)

    class Meta:
        verbose_name = 'mesa'
        verbose_name_plural = 'mesas'
        unique_together = ('name', 'date_time',)

    def __str__(self):
        return self.name


class Conference(models.Model):
    name = models.CharField('NOMBRE', max_length=200)
    date_time = models.DateTimeField(verbose_name="FECHA Y HORA", default=now, blank=True, null=True)
    youtube_url = models.URLField('Link de YouTube', null=True, blank=True)
    zoom_url = models.URLField('Link de Zoom', null=True, blank=True)
    observation = models.TextField(_("observación"), blank=True)

    def short_observation(self):
        return truncatechars(self.observation, 300)
    short_observation.short_description = _('observación')
    short_observation.allow_tags = True

    @property
    def date_time_localize(self):
        return localize(self.date_time)

    @property
    def youtube_url_embed(self):
        return youtube_url_to_embed(self.youtube_url)

    class Meta:
        verbose_name = 'conferencia'
        verbose_name_plural = 'Conferencias'
        unique_together = ('name', 'date_time',)

    def __str__(self):
        return self.name


class Workshop(models.Model):
    title = models.CharField('TÍTULO', max_length=200)
    date_time = models.DateTimeField(verbose_name="FECHA Y HORA", default=now, blank=True, null=True)
    responsable = models.CharField("RESPONSABLE",  max_length=200, blank=False, null=True)
    technical_operator = models.CharField("operador técnico", max_length=200, blank=True, null=True)
    youtube_url = models.URLField('Link de YouTube', null=True, blank=True)
    zoom_url = models.URLField('Link de Zoom', null=True, blank=True)
    observation = models.TextField(_("observación"), blank=True)

    def short_observation(self):
        return truncatechars(self.observation, 300)

    short_observation.short_description = _('observación')
    short_observation.allow_tags = True

    @property
    def youtube_url_embed(self):
        return youtube_url_to_embed(self.youtube_url)

    @property
    def date_time_localize(self):
        return localize(localtime(self.date_time))

    class Meta:
        verbose_name = 'taller'
        verbose_name_plural = 'talleres'
        unique_together = ('title', 'date_time',)

    def __str__(self):
        return self.title


class Audience(models.Model):
    title = models.CharField('TÍTULO', max_length=200)
    date_time = models.DateTimeField(verbose_name="FECHA Y HORA", default=now, blank=True, null=True)
    youtube_url = models.URLField('Link de YouTube', null=True, blank=True)
    zoom_url = models.URLField('Link de Zoom', null=True, blank=True)
    commission = models.ForeignKey(Commission, on_delete=models.PROTECT, verbose_name='mesa', null=True, blank=True,
                                   related_name='commission_audience', )
    observation = models.TextField(_("observación"), blank=True)

    def short_observation(self):
        return truncatechars(self.observation, 300)
    short_observation.short_description = _('observación')
    short_observation.allow_tags = True

    @property
    def youtube_url_embed(self):
        return youtube_url_to_embed(self.youtube_url)

    class Meta:
        verbose_name = 'auditorio'
        verbose_name_plural = 'auditorios'
        unique_together = ('title', 'date_time',)

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(_("TÍTULO"), max_length=250, unique=True)
    image = models.ImageField(_('IMAGEN'), upload_to=auto_cleaned_path_stripped_uuid4, null=True, blank=True)
    abstract = models.TextField(_("RESUMEN"), blank=False, null=True)
    author = models.ForeignKey(Person, on_delete=models.PROTECT, verbose_name='RESPONSABLE',
                               related_name='author_project', null=True, blank=False)
    theme = models.CharField('eje', max_length=2, choices=Commission.THEME_CHOICES, null=True, blank=True)
    main_theme = models.CharField(_('EJE TEMÁTICO'), max_length=140, null=True, blank=True)
    tags = TaggableManager(verbose_name="palabras claves",
                           help_text="Proporcione una lista de palabras claves separadas por comas")

    REJECTED = 'Rejected'
    PENDING = 'Pendiente'
    REQUEST_FOR_CHANGES = 'RequestForChanges'
    APPROVED = 'Approved'
    REVIEWED = 'reviewed'

    STATUS_CHOICES = (
        (REJECTED, 'Rechazada'),
        (PENDING, 'Pendiente'),
        (REQUEST_FOR_CHANGES, 'Solicitud de cambios'),
        (REVIEWED, 'Revisado'),
        (APPROVED, 'Aprobado'),
    )
    status = models.CharField('estado', max_length=20, choices=STATUS_CHOICES, default=PENDING, )
    commission = models.ForeignKey(Commission, on_delete=models.PROTECT, verbose_name='mesa', null=True, blank=True,
                                   related_name='commission_presentation', )

    @property
    def author_email(self):
        return self.author.email

    @property
    def image_resource_url(self):
        if self.image:
            return "https://www.congresoextension.utn.edu.ar%s" % self.image.url
            #return "http://0.0.0.0:8888%s" % self.image.url
        return None

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return None

    @property
    def commission_date_time(self):
        if self.commission:
            return localize(localtime(self.commission.date_time))
        return "-"

    @property
    def commission_youtube_url(self):
        if self.commission and self.commission.youtube_url:
            return self.commission.youtube_url
        return "-"

    @property
    def commission_zoom_url(self):
        if self.commission and self.commission.zoom_url:
            return self.commission.zoom_url
        return "-"

    @property
    def commission_moderator(self):
        if self.commission and self.commission.moderator:
            return self.commission.moderator
        return "-"

    def commission_description(self):
        if self.commission:
            return format_html("""<p><b>Fecha:</b> {}<br><b>Link de YouTube:</b> {}<br><b>Link de Zoom:</b> {}<br><b>Moderador:</b> {}</p>""",
                               self.commission_date_time,
                               self.commission_youtube_url,
                               self.commission_zoom_url,
                               self.commission.moderator)
        return "-"
    commission_description.short_description = _('Descripción Mesa')
    commission_description.allow_tags = True

    @property
    def authors(self):
        return ProjectAuthor.objects.filter(project=self.pk)

    def image_tag(self):
        if self.image_url:
            return format_html("""<img src='{}' width='40'"/>""", self.image_url)
        return "-"
    image_tag.short_description = _('IMAGEN')
    image_tag.allow_tags = True

    def short_description(self):
        return truncatechars(self.abstract, 300)
    short_description.short_description = _('descripción')
    short_description.allow_tags = True

    def project_actions(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return format_html(
            '<a class="btnProjectActions" href="{}"><span class ="glyphicon glyphicon-pencil"></span></a>'
            '<a class="btnProjectActions" href="{}"><span class ="glyphicon glyphicon-remove"></span></a>',
            reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.pk,)),
            reverse("admin:%s_%s_delete" % (content_type.app_label, content_type.model), args=(self.pk,)),
        )

    project_actions.short_description = 'acciones'
    project_actions.allow_tags = True

    class Meta:
        verbose_name = 'proyecto'
        verbose_name_plural = 'proyectos'

    def __str__(self):
        return self.title


class ProjectAuthor(models.Model):
    email = models.EmailField(_('CORREO ELECTRÓNICO'), blank=False, null=True)
    first_name = models.CharField(_('NOMBRE'), max_length=150, blank=False, null=True)
    last_name = models.CharField(_('APELLIDO'), max_length=150, blank=False, null=True)

    PASSPORT = "Passport"
    DOCUMENT_TYPE_CHOICES = (
        (PASSPORT, 'Pasaporte'),
        ("DNI", 'Documento Nacional de Identidad -D.N.I.'),
        ("LC", 'Libreta Cívica - L.C.'),
        ('LE', 'Libreta de Enrolamiento - L.E.'),
    )

    document_type = models.CharField(_('TIPO DOCUMENTO'), max_length=15, choices=DOCUMENT_TYPE_CHOICES, null=True,
                                     blank=False)
    document_number = models.CharField(verbose_name="NÚMERO DOCUMENTO", max_length=60, null=True, blank=False)
    university = models.ForeignKey(University, on_delete=models.PROTECT, verbose_name='UNIVERSIDAD',
                                   related_name='university_project_Author', null=True, blank=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='proyecto',
                                related_name='projectAuthor_project', null=False, blank=False)
    observation = models.TextField(_("observación"), blank=True, null=True)

    class Meta:
        verbose_name = 'autor'
        verbose_name_plural = 'autores'
        unique_together = ('document_number', 'project', 'document_type')

    def __str__(self):
        return "%s %s - %s" % (self.first_name, self.last_name, self.document_number, )


class Presentation(Project):
    thematic = models.ForeignKey(Thematic, on_delete=models.PROTECT, verbose_name='eje temático', null=True, blank=False,
                                 related_name='project_talk')
    document = models.FileField('DOCUMENTO (Word)', upload_to=auto_cleaned_path_stripped_uuid4, null=True, blank=False,
                                validators=[ExtensionValidator(['doc', 'docx', 'odt', ])],
                                help_text="Solamente se permiten documentos de word")
    link_url = models.URLField(null=True, blank=True)

    @property
    def document_resource_url(self):
        if self.document:
            return "https://www.congresoextension.utn.edu.ar%s" % self.document.url
        return None

    class Meta:
        verbose_name = 'ponencia'
        verbose_name_plural = 'ponencias'


class VideoPoster(Project):
    video = models.FileField('VÍDEO o AUDIO', upload_to=auto_cleaned_path_stripped_uuid4, null=True,
                             blank=True, validators=[ExtensionValidator(['mp4', 'avi', 'mkv', 'flv', 'mov', 'wmv',
                                                                          'mp3', 'm4a', 'flac', 'ogg', 'wma', 'aac'])],
                             help_text="Solamente se permiten archivos de vídeo o audio")
    youtube_url = models.URLField('Link de YouTube', null=True, blank=True)

    @property
    def video_resource_url(self):
        if self.video:
            return "https://www.congresoextension.utn.edu.ar%s" % self.video.url
        return None

    @property
    def youtube_url_embed(self):
        return youtube_url_to_embed(self.youtube_url)

    class Meta:
        verbose_name = 'video poster'
        verbose_name_plural = 'videos posters'


class Poster(Project):

    class Meta:
        verbose_name = 'poster'
        verbose_name_plural = 'posters'


class NoteProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    author = models.ForeignKey(Person, verbose_name='autor', on_delete=models.PROTECT)
    date = models.DateTimeField('fecha', auto_now=True, editable=False)
    note = models.TextField('nota', blank=False)

    class Meta:
        verbose_name = 'nota'
        verbose_name_plural = 'notas'

    def __str__(self):
        return ""
