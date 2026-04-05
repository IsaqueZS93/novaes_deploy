from django.db import models
from apps.core.models import TimeStampedModel

class DailyExecution(TimeStampedModel):
    STATUS=[('ok','Executado'),('parcial','Parcial'),('nao_exec','Não executado')]
    planning=models.ForeignKey('planning.WeeklyPlanning',on_delete=models.SET_NULL,null=True,blank=True,related_name='executions')
    contract=models.ForeignKey('contracts.Contract',on_delete=models.CASCADE)
    service=models.ForeignKey('contracts.ContractService',on_delete=models.CASCADE)
    team=models.ForeignKey('teams.Team',on_delete=models.SET_NULL,null=True,blank=True)
    execution_date=models.DateField()
    location=models.CharField(max_length=120)
    executed_quantity=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    executed_daily=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    worked_hours=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    expected_value=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    actual_value=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    status=models.CharField(max_length=20,choices=STATUS,default='ok')
    non_execution_reason=models.TextField(blank=True)
    notes=models.TextField(blank=True)
    launched_by=models.ForeignKey('accounts.User',on_delete=models.SET_NULL,null=True)
    class Meta:
        ordering=['-execution_date']
