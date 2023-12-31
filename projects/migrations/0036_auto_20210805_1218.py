# Generated by Django 3.1.2 on 2021-08-05 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0035_auto_20210804_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('Rejected', 'Rechazada'), ('Pendiente', 'Pendiente'), ('RequestForChanges', 'Solicitud de cambios'), ('reviewed', 'Revisado'), ('Approved', 'Aprobado')], default='Pendiente', max_length=20, verbose_name='estado'),
        ),
    ]
