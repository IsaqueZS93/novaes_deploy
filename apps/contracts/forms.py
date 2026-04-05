from django import forms
from .models import Contract,ContractService
class ContractForm(forms.ModelForm):
    class Meta:
        model=Contract
        fields='__all__'
class ContractServiceForm(forms.ModelForm):
    class Meta:
        model=ContractService
        fields='__all__'
