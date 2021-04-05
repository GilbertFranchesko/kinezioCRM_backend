# Generated by Django 3.1.7 on 2021-04-05 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_user_specialist'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(default='null', verbose_name='Краткая биография'),
        ),
        migrations.AddField(
            model_name='user',
            name='cabinet',
            field=models.IntegerField(default=-1, verbose_name='Номер кабиента'),
        ),
    ]
