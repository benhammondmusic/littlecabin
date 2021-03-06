# Generated by Django 3.2 on 2021-05-10 15:10

from django.db import migrations

def apply_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.bulk_create([
        Group(name=u'admin'),
        Group(name=u'member'),
        Group(name=u'1-Hammy'),
        Group(name=u'2-Toby'),
        Group(name=u'3-Connie'),
        Group(name=u'4-Cherie'),
        Group(name=u'5-Tom'),
        Group(name=u'6-Chris'),
    ])

    

class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0016_swap_created'),
    ]

    operations = [
        migrations.RunPython(apply_migration)
    ]

