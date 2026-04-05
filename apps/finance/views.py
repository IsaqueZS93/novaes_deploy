from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import redirect, render

from .forms import CostExpenseForm, RevenueForm
from .models import CostExpense, Revenue


@login_required
def costs_list(request):
    rows = CostExpense.objects.select_related("contract", "service", "team", "category").order_by("-launch_date")
    total = rows.aggregate(v=Sum("value"))["v"] or 0
    return render(request, "finance/costs_list.html", {"rows": rows, "total": total})


@login_required
def costs_create(request):
    form = CostExpenseForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("finance_costs_list")
    return render(request, "partials/form_page.html", {"form": form, "title": "Novo custo/despesa"})


@login_required
def revenues_list(request):
    rows = Revenue.objects.select_related("contract", "service").order_by("-launch_date")
    totals = rows.aggregate(expected=Sum("expected_value"), billed=Sum("billed_value"), received=Sum("received_value"))
    return render(request, "finance/revenues_list.html", {"rows": rows, "totals": totals})


@login_required
def revenues_create(request):
    form = RevenueForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("finance_revenues_list")
    return render(request, "partials/form_page.html", {"form": form, "title": "Nova receita"})
