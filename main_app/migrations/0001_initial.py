# Generated by Django 3.2 on 2021-04-30 17:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(choices=[('0', 'TBD'), ('1', 'Hammy'), ('2', 'Toby'), ('3', 'Connie'), ('4', 'Cherie'), ('5', 'Tom'), ('6', 'Chris')], default='0', max_length=1)),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
