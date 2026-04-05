from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    ADMIN='admin'; MANAGER='gestor'; OPS='operacional'; FIN='financeiro'; VIEW='visualizacao'
    CHOICES=[(ADMIN,'Administrador'),(MANAGER,'Gestor'),(OPS,'Operacional'),(FIN,'Financeiro'),(VIEW,'Visualização')]
    name=models.CharField(max_length=30,choices=CHOICES,unique=True)
    description=models.TextField(blank=True)
    def __str__(self):
        return self.get_name_display()

class User(AbstractUser):
    full_name=models.CharField(max_length=255,blank=True)
    role=models.ForeignKey(Role,on_delete=models.PROTECT,null=True,blank=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.full_name or self.username
