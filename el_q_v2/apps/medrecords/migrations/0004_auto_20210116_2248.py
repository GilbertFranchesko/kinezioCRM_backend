# Generated by Django 3.1.2 on 2021-01-16 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medrecords', '0003_medrecord_active_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medrecord',
            name='doctor',
            field=models.IntegerField(default=0, verbose_name='ID врача'),
        ),
        migrations.AlterField(
            model_name='medrecord',
            name='patient',
            field=models.IntegerField(default=0, verbose_name='ID пациента'),
        ),
    ]
