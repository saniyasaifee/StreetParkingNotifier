from django import forms
from .models import EmailAlert
from registration.forms import RegistrationForm

'''this is used to create an email form from the class'''
class EmailAlertForm(forms.ModelForm):
    class Meta:# pylint: disable=C1001,R0903,W0232
        model = EmailAlert
