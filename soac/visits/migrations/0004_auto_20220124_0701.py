# Generated by Django 3.2.9 on 2022-01-24 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0003_act'),
    ]

    operations = [
        migrations.AlterField(
            model_name='act',
            name='links',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='act',
            name='subsidies_what',
            field=models.CharField(default='0', max_length=255),
        ),
    ]
