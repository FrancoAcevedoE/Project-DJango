# Generated by Django 3.1.2 on 2021-09-06 14:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0041_workshop_technical_operator'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='NOMBRE')),
                ('date_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='FECHA Y HORA')),
                ('youtube_url', models.URLField(blank=True, null=True, verbose_name='Link de YouTube')),
                ('zoom_url', models.URLField(blank=True, null=True, verbose_name='Link de Zoom')),
                ('observation', models.TextField(blank=True, verbose_name='observación')),
            ],
            options={
                'verbose_name': 'conferencia',
                'verbose_name_plural': 'Conferencias',
                'unique_together': {('name', 'date_time')},
            },
        ),
    ]