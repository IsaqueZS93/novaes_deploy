from django import forms
from apps.clients.models import Client
from apps.contracts.models import Contract
from apps.teams.models import Team


class DashboardFilterForm(forms.Form):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), required=False)
    contract = forms.ModelChoiceField(queryset=Contract.objects.all(), required=False)
    team = forms.ModelChoiceField(queryset=Team.objects.all(), required=False)
    date_start = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    date_end = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
