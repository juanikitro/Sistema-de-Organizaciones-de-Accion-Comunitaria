from django.db import models
from django.contrib.auth.models import User 

class Profile(models.Model):
    #Choices
    ADMIN = 'AD'
    CENTRAL = 'CE'
    COMUNAL = 'CO'
    PRESIDENTE = 'PR'
    LEVELS = [
        (ADMIN, 'Administrador de SOAC'),
        (CENTRAL, 'Usuario de sede central'),
        (COMUNAL, 'Usuario de sede comunal'),
        (PRESIDENTE, 'Presidente'),
    ]

    # 1:1 con User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    #Importante
    level = models.CharField(
        max_length=2,
        choices=LEVELS,
        default=COMUNAL,
    )

    #Extras
    mobile = models.CharField(blank = True, null = True, max_length = 255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
