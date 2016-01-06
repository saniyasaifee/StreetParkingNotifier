from django import forms
from .models import Location
#from django.contrib.localflavor.us.forms import USPhoneNumberField

class LocationForm(forms.ModelForm):
    '''
    Location Form
    '''
    class Meta:
        ''' Meta class for Location'''
        model=Location
        exclude = ['user', 'status', 'signid', 'direction', 'latitude', 'longitude', 'main_street', 'from_street', 'boroughcode', 'to_street','signdesc']
       
class LocationInitForm(forms.Form):
    '''
    Location Initial form
    '''
    latitude = forms.DecimalField(widget=forms.HiddenInput())
    longitude = forms.DecimalField(widget=forms.HiddenInput())
        
