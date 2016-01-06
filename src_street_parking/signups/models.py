from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

'''This module is used to implement the email fields for email feature'''
class EmailAlert(models.Model):
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="Email")
    message = models.CharField(max_length=100, null=True, blank=True, verbose_name="Message")
