from django.db import models
from apps.core.models import TimeStampedModel

class CostCategory(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description=models.TextField(blank=True)
    def __str__(self): return self.name

class CostExpense(TimeStampedModel):
    contract=models.ForeignKey('contracts.Contract',on_delete=models.CASCADE)
    service=models.ForeignKey('contracts.ContractService',on_delete=models.SET_NULL,null=True,blank=True)
    team=models.ForeignKey('teams.Team',on_delete=models.SET_NULL,null=True,blank=True)
    category=models.ForeignKey(CostCategory,on_delete=models.PROTECT)
    launch_date=models.DateField()
    competence=models.DateField()
    description=models.CharField(max_length=255)
    supplier=models.CharField(max_length=120,blank=True)
    value=models.DecimalField(max_digits=14,decimal_places=2)
    cost_center=models.ForeignKey('core.CenterCost',on_delete=models.SET_NULL,null=True,blank=True)
    payment_method=models.CharField(max_length=60,blank=True)
    notes=models.TextField(blank=True)

class Revenue(TimeStampedModel):
    STATUS=[('previsto','Previsto'),('medicao','Em medição'),('faturado','Faturado'),('recebido','Recebido'),('atrasado','Atrasado'),('cancelado','Cancelado')]
    contract=models.ForeignKey('contracts.Contract',on_delete=models.CASCADE)
    service=models.ForeignKey('contracts.ContractService',on_delete=models.SET_NULL,null=True,blank=True)
    launch_date=models.DateField()
    competence=models.DateField()
    origin=models.CharField(max_length=120)
    expected_value=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    billed_value=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    received_value=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    status=models.CharField(max_length=20,choices=STATUS,default='previsto')
    notes=models.TextField(blank=True)
