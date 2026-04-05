from django import forms
from .models import DailyExecution
class DailyExecutionForm(forms.ModelForm):
    class Meta:
        model=DailyExecution
        fields='__all__'
        widgets={'execution_date':forms.DateInput(attrs={'type':'date'})}
