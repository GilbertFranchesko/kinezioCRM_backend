# Generated by Django 3.1.7 on 2021-04-21 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medrecords', '0022_auto_20210415_0158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medrecord',
            name='medications',
            field=models.TextField(default='None'),
        ),
    ]
