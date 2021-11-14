from django.db import models
from django.contrib.auth.models import User 

class Profile(models.Model):
    # 1:1 con User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    #Opcionales
    celular = models.CharField(blank = True, null = True, max_length = 255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.user.username