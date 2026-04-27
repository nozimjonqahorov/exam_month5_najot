from django.shortcuts import render, redirect
from django.views import View
from .forms import CategoryForm, TransactionForm
from .models import Category, Transaction
from django.db import transaction 
from django.contrib import messages
from .filters import TransactionFilter

class TransactionMainView(View):
    def get(self, request, form=None):
        queryset = Transaction.objects.filter(user=request.user).order_by('-date')
        f = TransactionFilter(request.GET, queryset=queryset, request=request)
        
        context = {
            "categories": Category.objects.filter(user=request.user),
            "transactions": f.qs, 
            "filter_form": f.form, 
            "t_form": form if form else TransactionForm(user=request.user),
            "c_form": CategoryForm(), # Kategoriya formasi esdan chiqmasin
        }
        return render(request, 'main_page.html', context)

    def post(self, request):
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            with transaction.atomic():
                new_t = form.save(commit=False)
                new_t.user = request.user
                account = new_t.account

                if new_t.type == 'xarajat' and account.balance < new_t.amount:
                    form.add_error('amount', f"Mablag' yetarli emas! Balans: {account.balance}")
                    return self.get(request, form=form)

                if new_t.type == 'daromad':
                    account.balance += new_t.amount
                else:
                    account.balance -= new_t.amount
                
                new_t.save()
                account.save()
                messages.success(request, "Tranzaksiya muvaffaqiyatli bajarildi!")
                return redirect('transaction_main')
        
        return self.get(request, form=form)

class CategoryCreatePostView(View):
    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data.get("name").strip().lower()
            category_type = form.cleaned_data.get("type")

            category, created = Category.objects.get_or_create(
                user=request.user, 
                name=category_name, 
                defaults={'type': category_type}
            )

            if not created:
                messages.warning(request, f"'{category_name}' kategoriyasi allaqachon mavjud.")
            else:
                messages.success(request, "Kategoriya qo'shildi.")
        
        return redirect('transaction_main') # Har qanday holatda redirect