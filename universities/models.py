from django.db import models


class University(models.Model):
    name = models.CharField('nombre', max_length=200)
    location = models.CharField('dirección', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Universidad / Organización'
        verbose_name_plural = 'Universidades / Organizaciones'

    def __str__(self):
        return self.name
