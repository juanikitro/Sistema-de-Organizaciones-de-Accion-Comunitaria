from django.db import models
from organizations.models import Org

class Activity(models.Model):
    activity_type = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    date= models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    hour= models.CharField(max_length=255, null=True, default='00:00:00')
    allday= models.CharField(max_length=3, null=True)

    orgs = models.ManyToManyField(Org) # Esto crea la tabla events_orgs