# Generated by Django 3.1.5 on 2021-01-23 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_notification_seen'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='from_user',
            new_name='doctor',
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='user',
            new_name='patient',
        ),
    ]
