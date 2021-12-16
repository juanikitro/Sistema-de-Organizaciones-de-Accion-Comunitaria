# Generated by Django 3.2.9 on 2021-12-16 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_org_registration_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='org',
            name='msg',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='org',
            name='registration_request',
            field=models.DateTimeField(null=True),
        ),
    ]
