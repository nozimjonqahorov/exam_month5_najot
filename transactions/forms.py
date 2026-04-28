from django import forms
from .models import Transaction, Category
from accounts.models import Account

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'type', 'amount', 'category', 'comment']


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['account'].queryset = Account.objects.filter(user=user)
            self.fields['category'].queryset = Category.objects.filter(user=user)
  
  
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        account = self.cleaned_data.get('account')

        if account:
            if account.currency == 'usd' and amount < 1:
                raise forms.ValidationError("Dollar hisobi uchun minimal o'tkazma $1")
            if account.currency == 'uzs' and amount < 1000:
                raise forms.ValidationError("So'm hisobi uchun minimal o'tkazma 1000 so'm")
        
        return amount
