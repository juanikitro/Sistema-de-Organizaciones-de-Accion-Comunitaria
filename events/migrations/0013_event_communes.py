# Generated by Django 3.2.9 on 2022-02-14 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_event_allday'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='communes',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
