from django.db import models
from apps.core.models import TimeStampedModel,ActiveModel

class Team(TimeStampedModel,ActiveModel):
    name=models.CharField(max_length=120,unique=True)
    leader=models.CharField(max_length=120)
    members=models.TextField(blank=True,help_text='Lista de membros separados por vírgula')
    operation_type=models.CharField(max_length=100,blank=True)
    contact=models.CharField(max_length=30,blank=True)
    notes=models.TextField(blank=True)
    def __str__(self): return self.name
