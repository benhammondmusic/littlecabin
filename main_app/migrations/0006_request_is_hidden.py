# Generated by Django 3.2 on 2021-05-03 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_rename_isdone_request_is_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='is_hidden',
            field=models.BooleanField(default=False),
        ),
    ]
