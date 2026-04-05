from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from .models import WeeklyPlanning
from .forms import WeeklyPlanningForm

@login_required
def calendar(request):
    return render(request,'planning/calendar.html',{'plans':WeeklyPlanning.objects.select_related('contract','service','team').all()})
@login_required
def create_plan(request):
    form=WeeklyPlanningForm(request.POST or None)
    if form.is_valid(): form.save(); return redirect('planning_calendar')
    return render(request,'partials/form_page.html',{'form':form,'title':'Novo item de planejamento'})
