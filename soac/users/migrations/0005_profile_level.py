# Generated by Django 3.2.9 on 2021-11-16 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_profile_celular'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='level',
            field=models.CharField(choices=[('AD', 'Administrador de SOAC'), ('CE', 'Usuario de sede central'), ('CO', 'Usuario de sede comunal'), ('PR', 'Presidente')], default='CO', max_length=2),
        ),
    ]
