from django.db.models import Sum,Count
from apps.contracts.models import Contract
from apps.planning.models import WeeklyPlanning
from apps.execution.models import DailyExecution
from apps.finance.models import CostExpense,Revenue


def dashboard_kpis():
    planned=WeeklyPlanning.objects.aggregate(v=Sum('planned_quantity'))['v'] or 0
    executed=DailyExecution.objects.aggregate(v=Sum('executed_quantity'))['v'] or 0
    expected_revenue=Revenue.objects.aggregate(v=Sum('expected_value'))['v'] or 0
    received_revenue=Revenue.objects.aggregate(v=Sum('received_value'))['v'] or 0
    total_cost=CostExpense.objects.aggregate(v=Sum('value'))['v'] or 0
    profit=received_revenue-total_cost
    margin=(profit/received_revenue*100) if received_revenue else 0
    return {
        'active_contracts':Contract.objects.filter(is_active=True,status='aberto').count(),
        'planned_total':planned,'executed_total':executed,'adherence':(executed/planned*100 if planned else 0),
        'expected_revenue':expected_revenue,'received_revenue':received_revenue,'total_cost':total_cost,'profit':profit,'margin':margin,
        'top_contracts':Contract.objects.annotate(exec_total=Count('services')).order_by('-exec_total')[:5]
    }
