# Generated by Django 3.1.7 on 2021-04-07 15:54

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medrecords', '0005_auto_20210123_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medrecord',
            name='training_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, size=None),
        ),
    ]
