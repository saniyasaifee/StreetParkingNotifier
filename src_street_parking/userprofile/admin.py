'''This module is for registering models'''
from django.contrib import admin
from userprofile.models import UserProfile

# Register your models here.

admin.site.register(UserProfile)
