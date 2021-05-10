# Generated by Django 3.2 on 2021-05-10 03:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0009_swap'),
    ]

    operations = [
        migrations.AddField(
            model_name='swap',
            name='desired_week',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main_app.week'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='swap',
            name='initiator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]