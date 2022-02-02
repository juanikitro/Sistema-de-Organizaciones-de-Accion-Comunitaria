from django.db import models
from django.db.models.fields import CharField

class Item(models.Model):
    action = CharField(default='', max_length=255)
    by = CharField(default='', max_length=255)
    date = models.DateTimeField(auto_now_add=True, null=True)