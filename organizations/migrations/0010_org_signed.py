# Generated by Django 3.2.9 on 2022-02-15 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0009_org_expiration_mail'),
    ]

    operations = [
        migrations.AddField(
            model_name='org',
            name='signed',
            field=models.CharField(default='No', max_length=10),
        ),
    ]
