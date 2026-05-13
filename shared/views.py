
from django.views import View
from django.shortcuts import render
from accounts.models import Account, Transfer
from .utils import get_exchange_rates, convert_currency
from django.views.generic import TemplateView
from django.db.models import Sum
from transactions.models import Transaction
from datetime import datetime, timedelta
from django.utils import timezone
from accounts.models import Transfer
from django.contrib.auth.mixins import LoginRequiredMixin

class HomepageView(LoginRequiredMixin, View):
    def get(self, request):
        transfers = Transfer.objects.filter(from_account__user = request.user).order_by("-date")[:5]
        transactions = Transaction.objects.filter(
            account__user=request.user
        ).select_related('category', 'account').order_by('-date')[:5]
        return render(request, "home.html", {"transfers":transfers, "transactions":transactions})


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user_accounts = Account.objects.filter(user=request.user)
        
        rates = get_exchange_rates() #kursni olamiz
        
        # Valyutani aniqlaymiz
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

        # Bu oyning daromad va xarajatlarini hisoblash
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
                monthly_expense -= amount_converted
        
        transfers = Transfer.objects.filter(from_account__user = request.user).order_by("-date")[:5]
        context = {
            'accounts': accounts_data,
            'total_balance': total_balance,
            'currency': display_currency,
            'rates': rates,
            'recent_transactions': recent_transactions,
            'monthly_income': round(monthly_income, 2),
            'monthly_expense': round(monthly_expense, 2),
            "transfers":transfers
        }
        return render(request, 'dashboard.html', context)

