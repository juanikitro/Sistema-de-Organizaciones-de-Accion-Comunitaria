# Generated by Django 3.2.9 on 2022-01-18 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_profile_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='commune',
            field=models.CharField(default='-', max_length=255),
            preserve_default=False,
        ),
    ]