# Generated by Django 3.1.2 on 2020-10-28 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0008_auto_20201026_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True, verbose_name='email address'),
        ),
    ]