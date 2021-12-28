from django.db import models
from organizations.models import Org

class Visit(models.Model):
    created= models.DateTimeField(auto_now_add=True, null=True)
    date= models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    hour= models.CharField(max_length=255, null=True, default='00:00:00')
    observation= models.CharField(max_length=255, null=True)

    org = models.CharField(null=False, max_length=5000, default='0')
    org_name = models.CharField(null=False, max_length=255, default='0')