# from django.contrib import admin

# # Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register CustomUser with a basic UserAdmin interface
admin.site.register(CustomUser, UserAdmin)