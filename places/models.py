from django.db import models


class Country(models.Model):
    id = models.IntegerField('id', primary_key=True)
    name = models.CharField('nombre', max_length=200, unique=True)
    alpha2 = models.CharField('alpha2', max_length=2, null=True, blank=True)
    alpha3 = models.CharField('alpha3', max_length=3, null=True, blank=True)

    class Meta:
        verbose_name = 'país'
        verbose_name_plural = 'países'

    def __str__(self):
        return self.name
