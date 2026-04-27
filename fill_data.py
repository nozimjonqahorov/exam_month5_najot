import os
import django
import random
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

# Django sozlamalarini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from transactions.models import Transaction, Category
from accounts.models import Account
from users.models import CustomUser

def generate_test_data(username, count=100):
    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        print(f"Foydalanuvchi {username} topilmadi!")
        return

    accounts = Account.objects.filter(user=user)
    categories = Category.objects.filter(user=user)

    if not accounts.exists() or not categories.exists():
        print("Sizda kamida bitta hisob va kategoriya bo'lishi kerak!")
        return

    types = ['daromad', 'xarajat']
    
    print(f"{count} ta tranzaksiya yaratilmoqda...")

    for i in range(count):
        t_type = random.choice(types)
        # Oxirgi 30 kun ichidagi tasodifiy sana
        random_days = random.randint(0, 30)
        random_hours = random.randint(0, 23)
        date = timezone.now() - timedelta(days=random_days, hours=random_hours)
        
        amount = Decimal(random.randrange(1000, 500000, 1000))
        
        Transaction.objects.create(
            user=user,
            account=random.choice(accounts),
            category=random.choice(categories.filter(type=t_type)),
            amount=amount,
            type=t_type,
            date=date,
            comment=f"Test tranzaksiya #{i+1}"
        )

    print("Tayyor! Ma'lumotlar muvaffaqiyatli qo'shildi.")

if __name__ == "__main__":
    # O'zingizning username-ingizni yozing (masalan: 'nozim')
    generate_test_data('nozim', 100)