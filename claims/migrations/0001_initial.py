# Generated by Django 3.2.9 on 2022-01-18 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('observation', models.CharField(default='0', max_length=255)),
                ('org', models.CharField(default='0', max_length=2500)),
                ('org_name', models.CharField(default='0', max_length=255)),
            ],
        ),
    ]
