from django.db import models
from users.models import CustomUser
from accounts.models import Account
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

class Category(models.Model):
    TYPES = [
        ("daromad", "DAROMAD"),
        ("xarajat", "XARAJAT")
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="categories", null=True, blank=True)
    name = models.CharField(max_length=40)
    type = models.CharField(max_length=20, choices=TYPES)
   
    class Meta:
        unique_together = (('user', 'name'),)

    def __str__(self):
        return self.name
    

class Transaction(models.Model):
    TYPES = [
        ("daromad", "DAROMAD"),
        ("xarajat", "XARAJAT")
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="transactions")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="account_transactions")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="category_transactions")
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    type = models.CharField(max_length=20, choices=TYPES)
    date = models.DateTimeField(default=timezone.now)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} | {self.amount} | {self.category} | {self.date}"
    

