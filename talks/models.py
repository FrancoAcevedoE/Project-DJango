from django.db import models
from django.utils.html import format_html
from django.utils import timezone
from django.template.defaultfilters import truncatechars
from django.utils.translation import gettext_lazy as _
from django_upload_path.upload_path import auto_cleaned_path_stripped_uuid4

from persons.models import Person


class Room(models.Model):
    name = models.CharField('nombre', max_length=200)

    class Meta:
        verbose_name = 'sala'
        verbose_name_plural = 'salas'

    def __str__(self):
        return self.name


class Day(models.Model):
    name = models.CharField('nombre', max_length=200)
    date = models.DateField(verbose_name="fecha", default=timezone.now)
    active = models.BooleanField(verbose_name="día activo", default=False)

    class Meta:
        verbose_name = 'día'
        verbose_name_plural = 'días'

    def __str__(self):
        return self.name

    @property
    def talks(self):
        return Talk.objects.filter(day=self.pk, is_masterful=False).order_by('start_time', 'end_time')

    @property
    def acts(self):
        return Act.objects.filter(day=self.pk).order_by('start_time', 'end_time')

    @property
    def masterfuls(self):
        return Talk.objects.filter(day=self.pk, is_masterful=True).order_by('start_time', 'end_time')

    @property
    def date_format(self):
        return self.date.strftime("%d de %B de %Y")

    @property
    def active_day(self):
        if self.active:
            return "active"
        return ""


class Talk(models.Model):
    title = models.CharField(_("titulo"), max_length=250, unique=True)
    logo = models.ImageField(_('logo'), upload_to=auto_cleaned_path_stripped_uuid4, null=True, blank=True)
    description = models.TextField(_("descripción"), blank=True)
    start_time = models.TimeField(verbose_name="inicio", default=timezone.now)
    end_time = models.TimeField(verbose_name="finalización", default=timezone.now)
    speakers = models.ManyToManyField(Person, verbose_name="expositores", related_name="speakers", blank=False)
    day = models.ForeignKey(Day, on_delete=models.PROTECT, verbose_name='día', related_name='day_talk', null=True,
                            blank=False)
    room = models.ForeignKey(Room, on_delete=models.PROTECT, verbose_name='sala', related_name='rom_talk', null=True,
                             blank=True)
    link_url = models.URLField(null=True, blank=False)
    is_active = models.BooleanField(_('active'), default=True)
    is_masterful = models.BooleanField(_('es magistral'), default=False)

    def logo_tag(self):
        if self.logo:
            url_image = self.logo.url
            return format_html("""<img src='{}' width='40'"/>""", url_image)
        return "-"
    logo_tag.short_description = _('logo')
    logo_tag.allow_tags = True

    def short_description(self):
        return truncatechars(self.description, 300)
    short_description.short_description = _('descripción')
    short_description.allow_tags = True

    class Meta:
        verbose_name = 'charla'
        verbose_name_plural = 'charlas'

    def __str__(self):
        return self.title


class Act(models.Model):
    title = models.CharField(_("titulo"), max_length=250, unique=True)
    start_time = models.TimeField(verbose_name="inicio", default=timezone.now)
    end_time = models.TimeField(verbose_name="finalización", default=timezone.now)
    day = models.ForeignKey(Day, on_delete=models.PROTECT, verbose_name='día', related_name='day_act', null=True,
                            blank=False)
    link_url = models.URLField(null=True, blank=False)
    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        verbose_name = 'acto'
        verbose_name_plural = 'actos'

    def __str__(self):
        return self.title
