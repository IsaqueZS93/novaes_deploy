from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from .models import Contract,ContractService
from .forms import ContractForm,ContractServiceForm

@login_required
def list_contracts(request):
    return render(request,'contracts/list.html',{'contracts':Contract.objects.select_related('client').all()})
@login_required
def create_contract(request):
    form=ContractForm(request.POST or None)
    if form.is_valid(): form.save(); return redirect('contracts_list')
    return render(request,'partials/form_page.html',{'form':form,'title':'Novo contrato'})
@login_required
def detail_contract(request,pk):
    c=get_object_or_404(Contract,pk=pk)
    return render(request,'contracts/detail.html',{'contract':c,'services':c.services.all()})
@login_required
def add_service(request,contract_id):
    form=ContractServiceForm(request.POST or None,initial={'contract':contract_id})
    if form.is_valid(): form.save(); return redirect('contracts_detail',pk=contract_id)
    return render(request,'partials/form_page.html',{'form':form,'title':'Novo serviço do contrato'})
