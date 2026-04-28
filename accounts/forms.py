from django import forms
from .models import Account, Transfer
from decimal import Decimal
class AccountCreateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'type', 'currency', 'balance', 'card_number']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bank nomi'
            }),
            'type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'currency': forms.Select(attrs={
                'class': 'form-select'
            }),
            'balance': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00'
            }),
            'card_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '1234 5678 9012 3456',
                'maxlength': '16'
            }),
        }


class TransferCreateForm(forms.Form):
    amount = forms.DecimalField(min_value=Decimal("0.01"), max_digits=12, decimal_places=2)

   