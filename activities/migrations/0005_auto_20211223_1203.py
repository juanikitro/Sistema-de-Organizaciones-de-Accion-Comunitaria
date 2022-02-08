# Generated by Django 3.2.9 on 2021-12-23 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_auto_20211216_1055'),
        ('activities', '0004_alter_activity_hour'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='activity_org',
        ),
        migrations.AddField(
            model_name='activity',
            name='orgs',
            field=models.ManyToManyField(to='organizations.Org'),
        ),
    ]