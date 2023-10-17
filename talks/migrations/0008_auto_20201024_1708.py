# Generated by Django 3.1.2 on 2020-10-24 20:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0007_talk_is_masterful'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='nombre')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='fecha')),
            ],
            options={
                'verbose_name': 'sala',
                'verbose_name_plural': 'salas',
            },
        ),
        migrations.RemoveField(
            model_name='talk',
            name='end_date_time',
        ),
        migrations.RemoveField(
            model_name='talk',
            name='start_date_time',
        ),
        migrations.AddField(
            model_name='talk',
            name='end_time',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='finalización'),
        ),
        migrations.AddField(
            model_name='talk',
            name='start_time',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='inicio'),
        ),
        migrations.AddField(
            model_name='talk',
            name='day',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='day_talk', to='talks.day', verbose_name='día'),
        ),
    ]