# Generated by Django 3.2.9 on 2021-11-18 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_active',
        ),
    ]
