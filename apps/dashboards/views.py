import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import DashboardFilterForm
from .services import dashboard_kpis


@login_required
def home(request):
    form = DashboardFilterForm(request.GET or None)
    filters = form.cleaned_data if form.is_valid() else {}
    kpis = dashboard_kpis(filters)

    trend_labels = [item["month"] for item in kpis["trend"]]
    trend_revenue = [item["revenue"] for item in kpis["trend"]]
    trend_cost = [item["cost"] for item in kpis["trend"]]

    return render(
        request,
        "dashboards/home.html",
        {
            "kpis": kpis,
            "filter_form": form,
            "trend_labels": json.dumps(trend_labels),
            "trend_revenue": json.dumps(trend_revenue),
            "trend_cost": json.dumps(trend_cost),
            "revenue_contract_labels": json.dumps([r["contract__name"] for r in kpis["revenue_by_contract"]]),
            "revenue_contract_values": json.dumps([float(r["total"] or 0) for r in kpis["revenue_by_contract"]]),
            "cost_category_labels": json.dumps([c["category__name"] for c in kpis["costs_by_category"]]),
            "cost_category_values": json.dumps([float(c["total"] or 0) for c in kpis["costs_by_category"]]),
        },
    )
