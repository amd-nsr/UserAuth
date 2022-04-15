from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    phone_number = models.CharField(unique=True, max_length=8)
  
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number
