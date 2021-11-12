from django.db import models
from django.contrib.auth.models import User 

class Usuario(models.Model):
    # 1:1 con User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # USERNAME_FIELD = 'cuit'
    
    # Importantes
    cuit = models.IntegerField(unique = True)
    email = models.EmailField(unique = True, max_length = 25)

    #Obligatorios
    nombre = models.CharField(max_length = 25)

    #Opcionales
    celular = models.IntegerField('Numero telefonico', blank = True, null = True)

    def __str__(self):
        return self.user.username