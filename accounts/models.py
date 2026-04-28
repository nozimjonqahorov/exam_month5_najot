from django.db import models
from users.models import CustomUser
from creditcards.models import CardNumberField
class Account(models.Model):
    """Hisob raqam"""
    NAMES = [
        ("visa", "VISA"),
        ("humo", "HUMO"),
        ("uzcard", "UZCARD"),
 
    ]

    CURRENCY = [
        ("uzs", "UZS"),
        ("usd", "USD")
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="accounts")
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=20, choices=NAMES)
    currency = models.CharField(max_length=30, choices=CURRENCY, default="uzs")
    balance = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    card_number = CardNumberField(unique = True, help_text="16 xonali karta raqamini kiriting")
   
    def __str__(self):
       return f"{self.name} | {self.currency}"
    
    class Meta:
        constraints = [
                models.CheckConstraint(
                    condition=models.Q(balance__gte=0), 
                    name="balance_negative_bolmasin"
                ),
            ]


class Transfer(models.Model):
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfer_out')
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfer_in')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"from {self.from_account.name} to {self.to_account.name}"




