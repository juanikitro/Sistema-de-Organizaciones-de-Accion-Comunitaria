# Generated by Django 3.2.9 on 2021-12-21 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_event_finished'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='finished',
        ),
    ]
