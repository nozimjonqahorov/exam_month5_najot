from django import forms
from .models import Account

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

