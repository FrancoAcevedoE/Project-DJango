# Generated by Django 3.1.2 on 2021-05-27 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_auto_20210527_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectauthor',
            name='document_type',
            field=models.CharField(choices=[('Passport', 'Pasaporte'), ('DNI', 'Documento Nacional de Identidad -D.N.I.'), ('LC', 'Libreta Cívica - L.C.'), ('LE', 'Libreta de Enrolamiento - L.E.')], max_length=15, null=True, verbose_name='TIPO DOCUMENTO'),
        ),
    ]
