# Generated by Django 3.2.9 on 2022-01-20 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='org',
            field=models.CharField(default='0', max_length=5000),
        ),
        migrations.AddField(
            model_name='visit',
            name='org_name',
            field=models.CharField(default='0', max_length=255),
        ),
    ]