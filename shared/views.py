
from django.views import View
from django.shortcuts import render
from accounts.models import Account
from .utils import get_exchange_rates, convert_currency
from django.views.generic import TemplateView
from django.db.models import Sum
from transactions.models import Transaction
from datetime import datetime, timedelta
from django.utils import timezone

class HomepageView(TemplateView):
    template_name = "home.html"



class DashboardView(View):
    def get(self, request):
        # 1. Foydalanuvchining hamma hisoblarini olamiz
        user_accounts = Account.objects.filter(user=request.user)
        
        # 2. API-dan kurslarni olamiz
        rates = get_exchange_rates()
        
        # 3. Valyutani aniqlaymiz
        display_currency = request.GET.get('currency', 'UZS').upper()
        
        total_balance = 0
        accounts_data = []

        for acc in user_accounts:
            converted_amount = convert_currency(acc.balance, acc.currency, display_currency, rates)
            total_balance += converted_amount
            
            accounts_data.append({
                'object': acc,
                'converted_balance': converted_amount
            })

        recent_transactions = Transaction.objects.filter(
            account__user=request.user
        ).select_related('category', 'account').order_by('-date')[:5]

        # 5. Bu oyning daromad va xarajatlarini hisoblash
        today = timezone.now()
        first_day_of_month = today.replace(day=1)
        
        monthly_income = 0
        monthly_expense = 0
        
        monthly_transactions = Transaction.objects.filter(
            account__user=request.user,
            date__gte=first_day_of_month
        )
        
        for trans in monthly_transactions:
            amount_converted = convert_currency(
                trans.amount, 
                trans.account.currency, 
                display_currency, 
                rates
            )
            
            if trans.type == 'daromad':
                monthly_income += amount_converted
            else:
                monthly_expense += amount_converted

        context = {
            'accounts': accounts_data,
            'total_balance': total_balance,
            'currency': display_currency,
            'rates': rates,
            'recent_transactions': recent_transactions,
            'monthly_income': round(monthly_income, 2),
            'monthly_expense': round(monthly_expense, 2),
        }
        return render(request, 'dashboard.html', context)
