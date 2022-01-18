from django.db import models

class Claim(models.Model):
    created= models.DateTimeField(auto_now_add=True, null=True)
    observation= models.CharField(max_length=255, null=False, default='0')
    state= models.CharField(max_length=255, null=False, default='abierto')
    by= models.CharField(max_length=255, null=False, default='0')

    org = models.CharField(null=False, max_length=2500, default='0')
    org_name = models.CharField(null=False, max_length=255, default='0')