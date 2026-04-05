from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import PlanningFilterForm, WeeklyPlanningForm
from .models import WeeklyPlanning
from .services import planning_vs_execution_rows


@login_required
def calendar(request):
    form = PlanningFilterForm(request.GET or None)
    qs = WeeklyPlanning.objects.select_related("contract", "service", "team").order_by("planned_date")

    if form.is_valid():
        if form.cleaned_data.get("contract"):
            qs = qs.filter(contract=form.cleaned_data["contract"])
        if form.cleaned_data.get("service"):
            qs = qs.filter(service=form.cleaned_data["service"])
        if form.cleaned_data.get("team"):
            qs = qs.filter(team=form.cleaned_data["team"])
        if form.cleaned_data.get("status"):
            qs = qs.filter(status=form.cleaned_data["status"])
        if form.cleaned_data.get("date_start"):
            qs = qs.filter(planned_date__gte=form.cleaned_data["date_start"])
        if form.cleaned_data.get("date_end"):
            qs = qs.filter(planned_date__lte=form.cleaned_data["date_end"])

    week_start = timezone.localdate() - timedelta(days=timezone.localdate().weekday())
    week_end = week_start + timedelta(days=6)
    weekly_rows = qs.filter(planned_date__range=[week_start, week_end])

    return render(
        request,
        "planning/calendar.html",
        {
            "plans": qs[:300],
            "weekly_comparison": planning_vs_execution_rows(weekly_rows),
            "filter_form": form,
            "week_start": week_start,
            "week_end": week_end,
        },
    )


@login_required
def create_plan(request):
    form = WeeklyPlanningForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("planning_calendar")
    return render(
        request,
        "partials/form_page.html",
        {"form": form, "title": "Novo item de planejamento"},
    )
