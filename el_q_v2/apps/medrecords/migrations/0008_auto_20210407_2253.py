# Generated by Django 3.1.7 on 2021-04-07 19:53

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medrecords', '0007_medrecord_medications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medrecord',
            name='medications',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default='[]', size=None),
        ),
    ]
