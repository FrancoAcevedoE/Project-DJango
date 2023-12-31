# Generated by Django 3.1.2 on 2020-10-23 22:03

import django.utils.timezone
import django_upload_path.upload_path
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='nombre')),
            ],
            options={
                'verbose_name': 'sala',
                'verbose_name_plural': 'salas',
            },
        ),
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='titulo')),
                ('logo', models.ImageField(blank=True, null=True, upload_to=django_upload_path.upload_path.auto_cleaned_path_stripped_uuid4, verbose_name='logo')),
                ('description', models.TextField(blank=True, verbose_name='descripción')),
                ('start_date_time', models.DateTimeField(default=django.utils.timezone.now, help_text='Fecha que va a estar disponible el permiso', verbose_name='inicio')),
                ('end_date_time', models.DateTimeField(help_text='Fecha que va a finalizar la autorización, en blanco no tiene fecha de finalización', verbose_name='finalización')),
                ('rom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='rom_talk', to='talks.rom', verbose_name='sala')),
                ('speaker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='speaker', to=settings.AUTH_USER_MODEL, verbose_name='expositor')),
            ],
            options={
                'verbose_name': 'charla',
                'verbose_name_plural': 'charlas',
            },
        ),
    ]
