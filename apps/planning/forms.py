from django import forms
from .models import WeeklyPlanning
class WeeklyPlanningForm(forms.ModelForm):
    class Meta:
        model=WeeklyPlanning
        fields='__all__'
        widgets={'planned_date':forms.DateInput(attrs={'type':'date'})}
