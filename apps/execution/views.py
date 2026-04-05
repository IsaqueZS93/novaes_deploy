from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from .forms import DailyExecutionForm
from .models import DailyExecution

@login_required
def list_execution(request):
    return render(request,'execution/list.html',{'rows':DailyExecution.objects.select_related('contract','service','team').all()})
@login_required
def create_execution(request):
    form=DailyExecutionForm(request.POST or None)
    if form.is_valid():
        obj=form.save(commit=False)
        obj.launched_by=request.user
        obj.save()
        return redirect('execution_list')
    return render(request,'partials/form_page.html',{'form':form,'title':'Novo lançamento diário'})
