# Generated by Django 3.2.9 on 2021-12-21 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visits', '0002_visit_hour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='hour',
            field=models.CharField(default='00:00:00', max_length=255, null=True),
        ),
    ]
