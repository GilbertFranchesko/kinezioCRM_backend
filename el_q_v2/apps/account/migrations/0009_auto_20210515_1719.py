# Generated by Django 3.1.7 on 2021-05-15 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20210405_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telegram_chat_id',
            field=models.IntegerField(default=0, verbose_name='ID чата телеграм'),
        ),
        migrations.AddField(
            model_name='user',
            name='telegram_id',
            field=models.IntegerField(default=0, verbose_name='ID телеграм'),
        ),
    ]
