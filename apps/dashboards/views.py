from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .services import dashboard_kpis

@login_required
def home(request):
    return render(request,'dashboards/home.html',{'kpis':dashboard_kpis()})
