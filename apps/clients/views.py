from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from .forms import ClientForm
from .models import Client

@login_required
def list_clients(request):
    q=request.GET.get('q','')
    qs=Client.objects.all()
    if q:
        qs=qs.filter(corporate_name__icontains=q)
    return render(request,'clients/list.html',{'clients':qs,'q':q})

@login_required
def create_client(request):
    form=ClientForm(request.POST or None)
    if form.is_valid():
        form.save(); return redirect('clients_list')
    return render(request,'partials/form_page.html',{'form':form,'title':'Novo cliente'})

@login_required
def edit_client(request,pk):
    obj=get_object_or_404(Client,pk=pk)
    form=ClientForm(request.POST or None,instance=obj)
    if form.is_valid():
        form.save(); return redirect('clients_list')
    return render(request,'partials/form_page.html',{'form':form,'title':'Editar cliente'})
