from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(null=True, blank=True, max_length=30)
    last_name = models.CharField(null=True, blank=True, max_length=30)
    country_code = models.CharField(null=True, blank=True, max_length=2)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    #phone_number = models.CharField(unique=True, max_length=11)
    # # List of genders 
    GENDER_CHOICES = [('1', 'Male'), ('2', 'Female')]
    gender = models.IntegerField(choices=GENDER_CHOICES, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True, max_length=200)
    email = models.EmailField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.first_name +" "+ self.last_name
