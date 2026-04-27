import django_filters
from django import forms
from .models import Transaction, Category
from accounts.models import Account

class TransactionFilter(django_filters.FilterSet):
    min_amount = django_filters.NumberFilter(field_name="amount", lookup_expr='gte', label="Min summa")
    max_amount = django_filters.NumberFilter(field_name="amount", lookup_expr='lte', label="Max summa")
    
    # Aynan shu yerda yoziladi:
    start_date = django_filters.DateFilter(
        field_name="date", 
        lookup_expr='date__gte', 
        label="Dan (sana)",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    end_date = django_filters.DateFilter(
        field_name="date", 
        lookup_expr='date__lte', 
        label="Gacha (sana)",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        # Viewdan kelayotgan requestni ajratib olamiz
        request = kwargs.pop('request', None)
        super(TransactionFilter, self).__init__(*args, **kwargs)
        
        if request:
            self.filters['category'].queryset = Category.objects.filter(user=request.user)
            self.filters['account'].queryset = Account.objects.filter(user=request.user)
    

    class Meta:
        model = Transaction
        # Qolgan oddiy filtrlarni ham shu yerda qoldirishingiz mumkin
        fields = ['type', 'category', 'account']