# Generated by Django 3.1.2 on 2020-10-24 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0005_auto_20201023_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
    ]
