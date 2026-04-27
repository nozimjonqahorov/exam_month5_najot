from django.contrib import admin
from .models import Transaction, Category

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = ('user', 'amount', 'type', 'date', "category")
    list_filter = ('type', 'date', 'category')
    search_fields = ('user__email', 'category__name')
    ordering = ["-id"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'type')
    list_filter = ('type', )
    search_fields = ('name', )
    ordering = ["-id"]
    
