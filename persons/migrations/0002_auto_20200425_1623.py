# Generated by Django 2.2.12 on 2020-04-25 19:23

from django.db import migrations, models
import django_upload_path.upload_path


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'persona', 'verbose_name_plural': 'personas'},
        ),
        migrations.AddField(
            model_name='person',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=django_upload_path.upload_path.auto_cleaned_path_stripped_uuid4, verbose_name='foto de perfil'),
        ),
    ]
