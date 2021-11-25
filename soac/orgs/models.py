from django.db import models

class Profile(models.Model):
    # Obligatorios
    name = models.CharField(max_length=255, unique=True)
    nhood = models.CharField(max_length=255, default='No especificado')
    commune = models.CharField(max_length=2, default='00')
    areas = models.CharField(max_length=255, default='No especificado')
    address

    # Opcionales
    public = models.CharField(max_length=255, default='No especificado')