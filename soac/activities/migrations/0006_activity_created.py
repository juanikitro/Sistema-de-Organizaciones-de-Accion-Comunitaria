# Generated by Django 3.2.9 on 2021-12-23 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_auto_20211223_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
