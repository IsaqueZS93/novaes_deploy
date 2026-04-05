from django import forms
from apps.contracts.models import Contract, ContractService
from apps.teams.models import Team
from .models import WeeklyPlanning


class WeeklyPlanningForm(forms.ModelForm):
    class Meta:
        model = WeeklyPlanning
        fields = "__all__"
        widgets = {
            "planned_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }


class PlanningFilterForm(forms.Form):
    contract = forms.ModelChoiceField(queryset=Contract.objects.all(), required=False)
    service = forms.ModelChoiceField(queryset=ContractService.objects.all(), required=False)
    team = forms.ModelChoiceField(queryset=Team.objects.all(), required=False)
    status = forms.ChoiceField(choices=[("", "Todos")] + WeeklyPlanning.STATUS, required=False)
    date_start = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    date_end = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
