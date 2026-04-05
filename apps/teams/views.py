from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from .forms import TeamForm
from .models import Team

@login_required
def list_teams(request):
    return render(request,'teams/list.html',{'teams':Team.objects.all()})
@login_required
def create_team(request):
    form=TeamForm(request.POST or None)
    if form.is_valid(): form.save(); return redirect('teams_list')
    return render(request,'partials/form_page.html',{'form':form,'title':'Nova equipe'})
