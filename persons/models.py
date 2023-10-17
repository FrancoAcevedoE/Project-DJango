from django.contrib.auth.models import User, AbstractUser
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.db import models
from django_upload_path.upload_path import auto_cleaned_path_stripped_uuid4

from places.models import Country
from universities.models import University


class Person(AbstractUser):
    email = models.EmailField(_('email address'), blank=False, null=True, unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)
    affiliation = models.CharField(_('Filiación'), max_length=150, null=True, blank=True)
    document_number = models.CharField(verbose_name="documento", max_length=60, null=True, blank=True)
    profile_picture = models.ImageField(_('foto de perfil'), upload_to=auto_cleaned_path_stripped_uuid4, null=True,
                                        blank=True)
    university = models.ForeignKey(University, on_delete=models.PROTECT, verbose_name='Universidad / Organización',
                                   related_name='university_person', null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name='país', related_name='country_person',
                                null=True, blank=True)
    this_payment = models.BooleanField(_('esta pago'), default=False, )
    description = models.TextField(_("descripción"), blank=True)

    ASSISTANT = 'Assistant'
    SPEAKER = 'Speaker'
    COLLABORATOR = 'Collaborator'
    EXTERNAL_COLLABORATOR = 'ExtColaborador'
    ORGANIZER = 'Organizer'
    EVALUATOR = 'Evaluator'

    USER_TYPE_CHOICES_COLLABORATOR = (
        (ASSISTANT, 'Asistente'),
        (SPEAKER, 'Ponente'),
        (EVALUATOR, 'Evaluador'),
    )

    USER_TYPE_CHOICES_ORGANIZER = (
        (ASSISTANT, 'Asistente'),
        (SPEAKER, 'Ponente'),
        (COLLABORATOR, 'Colaborador'),
        (EXTERNAL_COLLABORATOR, 'Colaborador externo'),
        (EVALUATOR, 'Evaluador'),
    )

    USER_TYPE_CHOICES = (
        (ASSISTANT, 'Asistente'),
        (SPEAKER, 'Ponente'),
        (EXTERNAL_COLLABORATOR, 'Colaborador externo'),
        (COLLABORATOR, 'Colaborador'),
        (ORGANIZER, 'Organizador'),
        (EVALUATOR, 'Evaluador'),
    )

    user_type = models.CharField(_('tipo'), max_length=15, choices=USER_TYPE_CHOICES, default=ASSISTANT)

    STUDENT = "Student"
    RELATION_CHOICES = (
        (STUDENT, 'Estudiante'),
        ("Graduate", 'Graduada/o'),
        ("Teacher", 'Docente'),
        ('NonTeaching', 'No Docente'),
        ('Community', 'Comunidad'),
    )

    relation = models.CharField(_('relación'), max_length=15, choices=RELATION_CHOICES, default=STUDENT, null=True,
                                blank=True)

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def profile_picture_short_tag(self):
        if self.profile_picture:
            url_image = self.profile_picture.url
            return format_html("""<img src='{}' width='40'"/>""", url_image)
        return "-"
    profile_picture_short_tag.short_description = _('vista previa')
    profile_picture_short_tag.allow_tags = True

    def profile_picture_medium_tag(self):
        if self.profile_picture:
            url_image = self.profile_picture.url
            return format_html("""<img src='{}' height='160'"/>""", url_image)
        return "-"
    profile_picture_medium_tag.short_description = _('foto de perfil')
    profile_picture_medium_tag.allow_tags = True

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'persona'
        verbose_name_plural = 'personas'

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        if not self.password:
            self.set_password(self.document_number)
        super(Person, self).save(*args, **kwargs)

    def __str__(self):
        if self.document_number:
            return "%s - %s" % (self.get_full_name(), self.document_number)
        else:
            return self.get_full_name()
