# Generated by Django 3.1.2 on 2021-04-23 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0015_auto_20210421_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='relation',
            field=models.CharField(blank=True, choices=[('Student', 'Estudiante'), ('Graduate', 'Graduada/o'), ('Teacher', 'Docente'), ('NonTeaching', 'No Docente'), ('Community', 'Comunidad')], default='Student', max_length=15, null=True, verbose_name='tipo'),
        ),
        migrations.AlterField(
            model_name='person',
            name='user_type',
            field=models.CharField(choices=[('Assistant', 'Asistente'), ('Speaker', 'Ponente'), ('ExtColaborador', 'Colaborador externo'), ('Collaborator', 'Colaborador'), ('Organizer', 'Organizador'), ('Evaluator', 'Evaluador')], default='Assistant', max_length=15, verbose_name='tipo'),
        ),
    ]