from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AccountCreateForm 
from .models import Account
from django.db.models import Prefetch
from transactions.models import Transaction
class AccountListView(LoginRequiredMixin, View):
    def get(self, request):
        accounts = Account.objects.filter(user = request.user)
        return render(request, "accounts_list.html", {"accounts":accounts})
    

class AccountCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = AccountCreateForm()
        return render(request, "account_create.html", {"form": form})
    
    def post(self, request):
        form = AccountCreateForm(request.POST)
        if form.is_valid():
            account = form.save(commit = False)
            account.user = request.user
            account.save()
            return redirect("accounts-list")
        return render(request, "account_create.html", {"form":form})
    

class AccountDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        tr_queryset = Transaction.objects.select_related('category').order_by('-date')

        queryset = Account.objects.prefetch_related(
            Prefetch('account_transactions', queryset=tr_queryset)
        ).filter(user=request.user)

        account = get_object_or_404(queryset, pk=pk)
        return render(request, "account_detail.html", {"account": account})
    
class AccountUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk): 
        account = get_object_or_404(Account, pk = pk, user = request.user)
        form  = AccountCreateForm(instance = account)
        return render(request, "account_update.html", {"form":form, "account":account})
    
    def post(self, request, pk):
        account = get_object_or_404(Account, pk = pk, user = request.user)
        form = AccountCreateForm(request.POST, instance = account)
        if form.is_valid():
            account = form.save(commit = False)
            account.user = request.user
            account.save()
            return redirect("account-detail", pk)
        return render(request, "account_update.html", {"form":form, "account":account})
    

class AccountDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        account = get_object_or_404(Account, pk = pk, user = request.user)
        return render(request, "account_delete.html", {"account":account})
    
    def post(self, request, pk):
        account = get_object_or_404(Account, pk = pk, user = request.user)
        account.delete()
        return redirect("accounts-list")
