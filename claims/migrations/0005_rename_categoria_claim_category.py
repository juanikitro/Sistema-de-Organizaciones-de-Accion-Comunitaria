# Generated by Django 3.2.9 on 2022-01-25 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0004_claim_categoria'),
    ]

    operations = [
        migrations.RenameField(
            model_name='claim',
            old_name='Categoria',
            new_name='category',
        ),
    ]
