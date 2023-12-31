# Generated by Django 3.1.2 on 2020-10-23 22:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_upload_path.upload_path
import projects.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Thematic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='nombre')),
            ],
            options={
                'verbose_name': 'temática',
                'verbose_name_plural': 'temáticas',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='título')),
                ('image', models.ImageField(blank=True, null=True, upload_to=django_upload_path.upload_path.auto_cleaned_path_stripped_uuid4, verbose_name='imágen')),
                ('description', models.TextField(blank=True, verbose_name='descripción')),
                ('document', models.FileField(help_text='Solamente se permiten documentos en pdf', upload_to=django_upload_path.upload_path.auto_cleaned_path_stripped_uuid4, validators=[projects.models.ExtensionValidator(['pdf'])], verbose_name='documento (PDF)')),
                ('link_url', models.URLField(null=True)),
                ('speaker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='speaker_project', to=settings.AUTH_USER_MODEL, verbose_name='expositor')),
                ('thematic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='project_talk', to='projects.thematic', verbose_name='temática')),
            ],
            options={
                'verbose_name': 'proyecto',
                'verbose_name_plural': 'proyectos',
            },
        ),
    ]
