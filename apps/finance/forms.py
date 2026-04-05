from django import forms
from .models import CostExpense,Revenue
class CostExpenseForm(forms.ModelForm):
    class Meta:
        model=CostExpense
        fields='__all__'
        widgets={'launch_date':forms.DateInput(attrs={'type':'date'}),'competence':forms.DateInput(attrs={'type':'date'})}
class RevenueForm(forms.ModelForm):
    class Meta:
        model=Revenue
        fields='__all__'
        widgets={'launch_date':forms.DateInput(attrs={'type':'date'}),'competence':forms.DateInput(attrs={'type':'date'})}
