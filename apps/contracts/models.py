from django.db import models
from apps.clients.models import Client
from apps.core.models import TimeStampedModel,ActiveModel,CenterCost

class ServiceCategory(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description=models.TextField(blank=True)
    def __str__(self): return self.name

class Contract(TimeStampedModel,ActiveModel):
    OPEN='aberto'; CLOSED='encerrado'; HOLD='suspenso'
    STATUS=[(OPEN,'Ativo'),(CLOSED,'Encerrado'),(HOLD,'Suspenso')]
    client=models.ForeignKey(Client,on_delete=models.PROTECT,related_name='contracts')
    name=models.CharField(max_length=255)
    number=models.CharField(max_length=60,unique=True)
    object=models.TextField()
    start_date=models.DateField()
    end_date=models.DateField()
    global_value=models.DecimalField(max_digits=14,decimal_places=2)
    cost_center=models.ForeignKey(CenterCost,on_delete=models.SET_NULL,null=True,blank=True)
    internal_manager=models.ForeignKey('accounts.User',on_delete=models.SET_NULL,null=True,blank=True)
    region=models.CharField(max_length=120,blank=True)
    status=models.CharField(max_length=20,choices=STATUS,default=OPEN)
    notes=models.TextField(blank=True)
    def __str__(self): return f'{self.number} - {self.name}'

class ContractService(TimeStampedModel,ActiveModel):
    UNIT='unidade'; DAILY='diaria'; HOUR='hora'; KM='km'; METER='metro'; MEASURE='medicao'; TEAMDAY='equipe_dia'; FIX='fixo'
    BILLING=[('unidade','Por unidade executada'),('diaria','Por diária'),('fixo','Valor fixo'),('periodo','Por período'),('medicao','Por medição'),('mista','Cobrança mista')]
    contract=models.ForeignKey(Contract,on_delete=models.CASCADE,related_name='services')
    category=models.ForeignKey(ServiceCategory,on_delete=models.SET_NULL,null=True,blank=True)
    name=models.CharField(max_length=255)
    description=models.TextField(blank=True)
    unit_measure=models.CharField(max_length=20,default=UNIT)
    billing_type=models.CharField(max_length=20,choices=BILLING,default='unidade')
    contracted_quantity=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    unit_value=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    daily_value=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    fixed_value=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    estimated_cost=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    execution_target=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    priority=models.PositiveSmallIntegerField(default=3)
    periodicity=models.CharField(max_length=30,blank=True)
    notes=models.TextField(blank=True)
    def __str__(self): return self.name
