# Generated by Django 3.2.9 on 2022-01-13 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_event_date_str'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='date_str',
        ),
    ]
