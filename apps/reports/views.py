from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from apps.execution.models import DailyExecution

@login_required
def index(request):
    data=DailyExecution.objects.select_related('contract','service','team')[:100]
    return render(request,'reports/index.html',{'rows':data})

@login_required
def print_report(request):
    return HttpResponse('Relatório para impressão - integrar PDF/Excel na fase 2.')
