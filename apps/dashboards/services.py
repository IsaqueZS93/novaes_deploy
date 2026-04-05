from collections import defaultdict
from datetime import date
from django.db.models import Sum

from apps.contracts.models import Contract
from apps.execution.models import DailyExecution
from apps.finance.models import CostExpense, Revenue
from apps.planning.models import WeeklyPlanning


def _apply_contract_scope(queryset, filters):
    contract = filters.get("contract")
    client = filters.get("client")
    if contract:
        queryset = queryset.filter(contract=contract)
    elif client:
        queryset = queryset.filter(contract__client=client)
    return queryset


def _apply_date_scope(queryset, field_name, filters):
    if filters.get("date_start"):
        queryset = queryset.filter(**{f"{field_name}__gte": filters["date_start"]})
    if filters.get("date_end"):
        queryset = queryset.filter(**{f"{field_name}__lte": filters["date_end"]})
    return queryset


def dashboard_kpis(filters=None):
    filters = filters or {}

    planning_qs = _apply_contract_scope(WeeklyPlanning.objects.all(), filters)
    planning_qs = _apply_date_scope(planning_qs, "planned_date", filters)
    if filters.get("team"):
        planning_qs = planning_qs.filter(team=filters["team"])

    execution_qs = _apply_contract_scope(DailyExecution.objects.all(), filters)
    execution_qs = _apply_date_scope(execution_qs, "execution_date", filters)
    if filters.get("team"):
        execution_qs = execution_qs.filter(team=filters["team"])

    revenue_qs = _apply_contract_scope(Revenue.objects.all(), filters)
    revenue_qs = _apply_date_scope(revenue_qs, "launch_date", filters)

    cost_qs = _apply_contract_scope(CostExpense.objects.all(), filters)
    cost_qs = _apply_date_scope(cost_qs, "launch_date", filters)

    planned = planning_qs.aggregate(v=Sum("planned_quantity"))["v"] or 0
    executed = execution_qs.aggregate(v=Sum("executed_quantity"))["v"] or 0
    expected_revenue = revenue_qs.aggregate(v=Sum("expected_value"))["v"] or 0
    received_revenue = revenue_qs.aggregate(v=Sum("received_value"))["v"] or 0
    total_cost = cost_qs.aggregate(v=Sum("value"))["v"] or 0
    profit = received_revenue - total_cost
    margin = (profit / received_revenue * 100) if received_revenue else 0

    revenue_by_contract = list(
        revenue_qs.values("contract__name").annotate(total=Sum("received_value")).order_by("-total")[:8]
    )
    costs_by_category = list(
        cost_qs.values("category__name").annotate(total=Sum("value")).order_by("-total")[:8]
    )

    monthly = defaultdict(lambda: {"revenue": 0, "cost": 0})
    for row in revenue_qs.values("launch_date").annotate(total=Sum("received_value")):
        month = row["launch_date"].strftime("%Y-%m") if row["launch_date"] else date.today().strftime("%Y-%m")
        monthly[month]["revenue"] += float(row["total"] or 0)
    for row in cost_qs.values("launch_date").annotate(total=Sum("value")):
        month = row["launch_date"].strftime("%Y-%m") if row["launch_date"] else date.today().strftime("%Y-%m")
        monthly[month]["cost"] += float(row["total"] or 0)

    trend = [
        {
            "month": month,
            "revenue": values["revenue"],
            "cost": values["cost"],
            "profit": values["revenue"] - values["cost"],
        }
        for month, values in sorted(monthly.items())
    ]

    return {
        "active_contracts": Contract.objects.filter(is_active=True, status="aberto").count(),
        "planned_total": planned,
        "executed_total": executed,
        "adherence": (executed / planned * 100 if planned else 0),
        "expected_revenue": expected_revenue,
        "received_revenue": received_revenue,
        "total_cost": total_cost,
        "profit": profit,
        "margin": margin,
        "revenue_by_contract": revenue_by_contract,
        "costs_by_category": costs_by_category,
        "trend": trend,
    }
