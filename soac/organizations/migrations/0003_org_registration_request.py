# Generated by Django 3.2.9 on 2021-12-14 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_org_enrolled'),
    ]

    operations = [
        migrations.AddField(
            model_name='org',
            name='registration_request',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
