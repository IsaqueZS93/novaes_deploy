from django.db.models import Sum
from apps.execution.models import DailyExecution


def planning_vs_execution_rows(planning_qs):
    rows = []
    for item in planning_qs:
        executed = (
            DailyExecution.objects.filter(planning=item).aggregate(v=Sum("executed_quantity"))["v"]
            or 0
        )
        rows.append(
            {
                "planning": item,
                "planned": item.planned_quantity,
                "executed": executed,
                "delta": executed - item.planned_quantity,
                "adherence": (executed / item.planned_quantity * 100)
                if item.planned_quantity
                else 0,
            }
        )
    return rows
