from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import DailyExecutionForm, ExecutionFilterForm
from .models import DailyExecution


@login_required
def list_execution(request):
    form = ExecutionFilterForm(request.GET or None)
    qs = DailyExecution.objects.select_related("contract", "service", "team", "planning")
    if form.is_valid():
        if form.cleaned_data.get("execution_date"):
            qs = qs.filter(execution_date=form.cleaned_data["execution_date"])
        if form.cleaned_data.get("contract"):
            qs = qs.filter(contract=form.cleaned_data["contract"])
        if form.cleaned_data.get("service"):
            qs = qs.filter(service=form.cleaned_data["service"])
        if form.cleaned_data.get("team"):
            qs = qs.filter(team=form.cleaned_data["team"])
        if form.cleaned_data.get("location"):
            qs = qs.filter(location__icontains=form.cleaned_data["location"])
    return render(request, "execution/list.html", {"rows": qs.order_by("-execution_date"), "filter_form": form})


@login_required
def create_execution(request):
    form = DailyExecutionForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.launched_by = request.user
        obj.save()
        return redirect("execution_list")
    return render(
        request,
        "partials/form_page.html",
        {"form": form, "title": "Novo lançamento diário"},
    )
