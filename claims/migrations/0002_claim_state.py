# Generated by Django 3.2.9 on 2022-01-18 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='claim',
            name='state',
            field=models.CharField(default='abierto', max_length=255),
        ),
    ]
