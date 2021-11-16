from django.db import models
from django.contrib.auth.models import User 

class Profile(models.Model):
    # 1:1 con User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # 1:1 con User sintetico
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    #Importante
    level = models.CharField(max_length=255)

    #Extras
    mobile = models.CharField(blank = True, null = True, max_length = 255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
