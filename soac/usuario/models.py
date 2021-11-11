from django.db import models
from django.contrib.auth.models import User 

class Usuario(models.Model):
    # 1:1 con User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    USERNAME_FIELD = 'cuit'
    
    # Importantes
    cuit = models.IntegerField('Cuit', unique = True)
    email = models.EmailField('Email', unique = True, max_length = 25)
    contrasena = models.IntegerField('Contrasena')

    #Obligatorios
    nombre = models.CharField('Nombre completo', max_length = 25)
    created=models.DateTimeField(auto_now_add=True, blank=False)
    
    #Opcionales
    celular = models.IntegerField('Numero telefonico', blank = True, null = True)

    def __str__(self):
        return self.user.nombre