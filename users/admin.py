from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = [('phone_number'),]
    #list_display = ['phone_number', 'email',]

admin.site.register(CustomUser, CustomUserAdmin)
