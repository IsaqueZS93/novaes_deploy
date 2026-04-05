from django.db import models
from apps.core.models import TimeStampedModel,ActiveModel

class Client(TimeStampedModel,ActiveModel):
    corporate_name=models.CharField(max_length=255)
    trade_name=models.CharField(max_length=255,blank=True)
    cnpj=models.CharField(max_length=18,unique=True)
    main_contact=models.CharField(max_length=120,blank=True)
    phone=models.CharField(max_length=25,blank=True)
    email=models.EmailField(blank=True)
    address=models.CharField(max_length=255,blank=True)
    city=models.CharField(max_length=120,blank=True)
    state=models.CharField(max_length=2,blank=True)
    notes=models.TextField(blank=True)
    class Meta:
        ordering=['corporate_name']
    def __str__(self): return self.corporate_name
