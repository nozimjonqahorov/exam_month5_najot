from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from transactions.models import Category # Faqat Category-ni olamiz

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_categories(sender, instance, created, **kwargs):
    if created:
        # Faqat siz aytgan default kategoriyalar
        default_categories = [
            ('oziq-ovqat', 'xarajat'),
            ('kiyim', 'xarajat'),
            ('transport', 'xarajat'),
            ('komunal', 'xarajat'),
            ('maosh', 'daromad'),
        ]
        
        for name, cat_type in default_categories:
            Category.objects.create(
                user=instance,
                name=name,
                type=cat_type
            )