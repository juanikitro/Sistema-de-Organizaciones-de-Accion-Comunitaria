from django.db import models
from claims.models import Claim

class Visit(models.Model):
    created= models.DateTimeField(auto_now_add=True, null=True)
    date= models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    hour= models.CharField(max_length=255, null=True, default='00:00:00')
    allday= models.CharField(max_length=3, null=True)
    observation= models.CharField(max_length=255, null=True)

    org = models.CharField(null=False, max_length=5000, default='0')
    org_name = models.CharField(null=False, max_length=255, default='0')

    act_id = models.CharField(null=True, default=0, max_length=255)

class Act(models.Model):
    created= models.DateTimeField(auto_now_add=True, null=True)
    date= models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    agent = models.CharField(max_length=255, null=False)
    receptor_name= models.CharField(max_length=255, null=False)
    receptor_charge= models.CharField(max_length=255, null=False)
    beneficiaries= models.CharField(max_length=255, null=False)
    partners= models.CharField(max_length=255, null=False)
    tasks= models.CharField(max_length=255, null=False)
    subsidies= models.CharField(max_length=2, null=False)
    subsidies_what= models.CharField(max_length=255, default='0')
    links= models.CharField(max_length=255, null=False)

    visit = models.OneToOneField(Visit, on_delete=models.CASCADE)
    claim_exist= models.CharField(max_length=3, null=False)
    claim = models.OneToOneField(Claim, on_delete=models.CASCADE)