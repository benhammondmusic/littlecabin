# Generated by Django 3.2 on 2021-05-03 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_agree_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='item',
            field=models.CharField(default='q', max_length=300),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='postcard',
            name='message',
            field=models.TextField(max_length=2000),
        ),
    ]
