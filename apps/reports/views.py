import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from apps.execution.models import DailyExecution


@login_required
def index(request):
    data = DailyExecution.objects.select_related("contract", "service", "team")[:200]
    return render(request, "reports/index.html", {"rows": data})


@login_required
def export_csv(request):
    rows = DailyExecution.objects.select_related("contract", "service", "team").order_by("-execution_date")
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="execucao_diaria.csv"'
    writer = csv.writer(response)
    writer.writerow([
        "Data",
        "Contrato",
        "Serviço",
        "Equipe",
        "Localidade",
        "Quantidade",
        "Valor Previsto",
        "Valor Realizado",
    ])
    for row in rows:
        writer.writerow(
            [
                row.execution_date,
                row.contract.number,
                row.service.name,
                row.team,
                row.location,
                row.executed_quantity,
                row.expected_value,
                row.actual_value,
            ]
        )
    return response
