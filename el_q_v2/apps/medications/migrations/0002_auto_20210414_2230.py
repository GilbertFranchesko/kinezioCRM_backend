# Generated by Django 3.1.7 on 2021-04-14 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medication',
            name='date',
        ),
        migrations.RemoveField(
            model_name='medication',
            name='dose',
        ),
        migrations.RemoveField(
            model_name='medication',
            name='finish_date',
        ),
        migrations.RemoveField(
            model_name='medication',
            name='time',
        ),
        migrations.AddField(
            model_name='medication',
            name='doctor',
            field=models.IntegerField(default=0, verbose_name='Доктор добавил'),
        ),
    ]
