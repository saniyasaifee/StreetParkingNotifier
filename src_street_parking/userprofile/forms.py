from django import forms
from django.contrib.auth.models import User
from userprofile.models import UserProfile

'''form foe the user to update the profile'''
class FormUserUpdate(forms.ModelForm): # pylint: disable=R0903
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

'''this is to used to create a form with phone number field'''
class FormUserProfileUpdate(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ( 'phoneNumber', )
    
