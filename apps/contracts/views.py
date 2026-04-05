from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContractForm, ContractServiceForm
from .models import Contract
from .services import contract_summary
from apps.planning.models import WeeklyPlanning
from apps.execution.models import DailyExecution
from apps.finance.models import CostExpense, Revenue


@login_required
def list_contracts(request):
    qs = Contract.objects.select_related("client", "cost_center", "internal_manager")
    status = request.GET.get("status")
    if status:
        qs = qs.filter(status=status)
    search = request.GET.get("q", "")
    if search:
        qs = qs.filter(name__icontains=search)
    return render(
        request,
        "contracts/list.html",
        {
            "contracts": qs.order_by("-created_at"),
            "status": status,
            "q": search,
            "status_choices": Contract.STATUS,
        },
    )


@login_required
def create_contract(request):
    form = ContractForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("contracts_list")
    return render(request, "partials/form_page.html", {"form": form, "title": "Novo contrato"})


@login_required
def detail_contract(request, pk):
    contract = get_object_or_404(Contract.objects.select_related("client"), pk=pk)
    tab = request.GET.get("tab", "resumo")
    context = {
        "contract": contract,
        "services": contract.services.all().order_by("priority"),
        "summary": contract_summary(contract),
        "tab": tab,
        "planning_rows": WeeklyPlanning.objects.filter(contract=contract).select_related(
            "service", "team"
        )[:30],
        "execution_rows": DailyExecution.objects.filter(contract=contract).select_related(
            "service", "team"
        )[:30],
        "cost_rows": CostExpense.objects.filter(contract=contract).select_related(
            "category", "service"
        )[:30],
        "revenue_rows": Revenue.objects.filter(contract=contract).select_related("service")[:30],
    }
    return render(request, "contracts/detail.html", context)


@login_required
def add_service(request, contract_id):
    form = ContractServiceForm(request.POST or None, initial={"contract": contract_id})
    if form.is_valid():
        service = form.save()
        return redirect(f"/contratos/{service.contract_id}/?tab=servicos")
    return render(
        request,
        "partials/form_page.html",
        {"form": form, "title": "Novo serviço do contrato"},
    )
