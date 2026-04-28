from django.contrib import admin
from .models import Account, Transfer

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):

    list_display = ('user', 'balance', 'type')
    list_filter = ("type", )
    ordering = ["-id"]
    search_fields = ("user__email", "user__first_name")


admin.site.register(Transfer)