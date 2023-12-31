# Generated by Django 3.1.2 on 2021-04-16 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='id')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='nombre')),
                ('alpha2', models.CharField(blank=True, max_length=2, null=True, verbose_name='alpha2')),
                ('alpha3', models.CharField(blank=True, max_length=3, null=True, verbose_name='alpha3')),
            ],
            options={
                'verbose_name': 'país',
                'verbose_name_plural': 'países',
            },
        ),
    ]
