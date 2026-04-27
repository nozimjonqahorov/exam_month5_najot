from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to="users/", default="users/default_user.png")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} | {self.last_name}"
    
    