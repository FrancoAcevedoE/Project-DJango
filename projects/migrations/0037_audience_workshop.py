# Generated by Django 3.1.2 on 2021-08-19 02:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0036_auto_20210805_1218'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='TÍTULO')),
                ('date_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='FECHA Y HORA')),
                ('youtube_url', models.URLField(blank=True, null=True, verbose_name='Link de YouTube')),
                ('zoom_url', models.URLField(blank=True, null=True, verbose_name='Link de Zoom')),
                ('observation', models.TextField(blank=True, verbose_name='observación')),
            ],
            options={
                'verbose_name': 'taller',
                'verbose_name_plural': 'talleres',
                'unique_together': {('title', 'date_time')},
            },
        ),
        migrations.CreateModel(
            name='Audience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='TÍTULO')),
                ('date_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='FECHA Y HORA')),
                ('youtube_url', models.URLField(blank=True, null=True, verbose_name='Link de YouTube')),
                ('zoom_url', models.URLField(blank=True, null=True, verbose_name='Link de Zoom')),
                ('observation', models.TextField(blank=True, verbose_name='observación')),
                ('commission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='commission_audience', to='projects.commission', verbose_name='mesa')),
            ],
            options={
                'verbose_name': 'auditorio',
                'verbose_name_plural': 'auditorios',
                'unique_together': {('title', 'date_time')},
            },
        ),
    ]