from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(null=False, blank=False, max_length=30)
    last_name = models.CharField(null=False, blank=False, max_length=30)
    country_code = models.CharField(null=False, blank=False, max_length=2)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    # # List of genders 
    GENDER_CHOICES = [('1', 'Male'), ('2', 'Female')]
    gender = models.IntegerField(choices=GENDER_CHOICES, blank=False, null=False)
    birthdate = models.DateField(blank=False, null=False)
    avatar = models.ImageField(upload_to='avatar/', null=False, blank=False, max_length=200)
    email = models.EmailField(max_length=255, unique=True, null=True, default=None)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.first_name +" "+ self.last_name
