from django.db import models
from apps.core.models import TimeStampedModel

class WeeklyPlanning(TimeStampedModel):
    STATUS=[('planejado','Planejado'),('andamento','Em andamento'),('concluido','Concluído'),('parcial','Parcial'),('reprogramado','Reprogramado'),('cancelado','Cancelado')]
    SHIFT=[('manha','Manhã'),('tarde','Tarde'),('noite','Noite'),('integral','Integral')]
    contract=models.ForeignKey('contracts.Contract',on_delete=models.CASCADE)
    service=models.ForeignKey('contracts.ContractService',on_delete=models.CASCADE)
    team=models.ForeignKey('teams.Team',on_delete=models.SET_NULL,null=True,blank=True)
    planned_date=models.DateField()
    shift=models.CharField(max_length=20,choices=SHIFT,default='integral')
    location=models.CharField(max_length=120)
    planned_quantity=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    priority=models.PositiveSmallIntegerField(default=3)
    status=models.CharField(max_length=20,choices=STATUS,default='planejado')
    notes=models.TextField(blank=True)
    class Meta:
        ordering=['planned_date']
