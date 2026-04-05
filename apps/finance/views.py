from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from .models import CostExpense,Revenue
from .forms import CostExpenseForm,RevenueForm

@login_required
def costs_list(request):
    return render(request,'finance/costs_list.html',{'rows':CostExpense.objects.select_related('contract','service','team','category').all()})
@login_required
def costs_create(request):
    form=CostExpenseForm(request.POST or None)
    if form.is_valid(): form.save(); return redirect('finance_costs_list')
    return render(request,'partials/form_page.html',{'form':form,'title':'Novo custo/despesa'})
@login_required
def revenues_list(request):
    return render(request,'finance/revenues_list.html',{'rows':Revenue.objects.select_related('contract','service').all()})
@login_required
def revenues_create(request):
    form=RevenueForm(request.POST or None)
    if form.is_valid(): form.save(); return redirect('finance_revenues_list')
    return render(request,'partials/form_page.html',{'form':form,'title':'Nova receita'})
