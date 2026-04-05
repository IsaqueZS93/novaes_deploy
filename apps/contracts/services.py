from django.db.models import Sum
from apps.execution.models import DailyExecution
from apps.finance.models import CostExpense, Revenue
from apps.planning.models import WeeklyPlanning


def contract_summary(contract):
    planned_qty = (
        WeeklyPlanning.objects.filter(contract=contract).aggregate(v=Sum("planned_quantity"))["v"]
        or 0
    )
    executed_qty = (
        DailyExecution.objects.filter(contract=contract).aggregate(v=Sum("executed_quantity"))["v"]
        or 0
    )
    revenue_expected = (
        Revenue.objects.filter(contract=contract).aggregate(v=Sum("expected_value"))["v"] or 0
    )
    revenue_received = (
        Revenue.objects.filter(contract=contract).aggregate(v=Sum("received_value"))["v"] or 0
    )
    cost_total = (
        CostExpense.objects.filter(contract=contract).aggregate(v=Sum("value"))["v"] or 0
    )
    profit = revenue_received - cost_total
    margin = (profit / revenue_received * 100) if revenue_received else 0

    return {
        "planned_qty": planned_qty,
        "executed_qty": executed_qty,
        "adherence": (executed_qty / planned_qty * 100) if planned_qty else 0,
        "revenue_expected": revenue_expected,
        "revenue_received": revenue_received,
        "cost_total": cost_total,
        "profit": profit,
        "margin": margin,
    }
