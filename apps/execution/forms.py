from django import forms
from apps.contracts.models import Contract, ContractService
from apps.teams.models import Team
from .models import DailyExecution


class DailyExecutionForm(forms.ModelForm):
    class Meta:
        model = DailyExecution
        fields = "__all__"
        widgets = {
            "execution_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 2}),
            "non_execution_reason": forms.Textarea(attrs={"rows": 2}),
        }


class ExecutionFilterForm(forms.Form):
    execution_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    contract = forms.ModelChoiceField(queryset=Contract.objects.all(), required=False)
    service = forms.ModelChoiceField(queryset=ContractService.objects.all(), required=False)
    team = forms.ModelChoiceField(queryset=Team.objects.all(), required=False)
    location = forms.CharField(required=False)
