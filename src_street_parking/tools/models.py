from django.db import models
from django.utils.encoding import smart_unicode
from django.contrib.auth.models import User
from django.forms import ModelForm
#from phonenumber_field.modelfields import PhoneNumberField

class AddPreferences(models.Model):
    prefermedium_list = (
        ('email','email'),
        ('text','text message'),
        ('call','phone call'),   
    )
    prefertime_list = (
        ('1h','1 hour'),
        ('2h','2 hours'),
        ('3h','3 hours'),   
    )
    
    #getting the user 
    user_prefer = models.ForeignKey(User)
    # create fields for settings page 
    Preference= models.CharField(max_length=100, choices=prefermedium_list, default='email')
    Notification = models.CharField(max_length=100, choices=prefertime_list, default='1h')
    #Phone=PhoneNumberField()
    Phone=models.IntegerField(max_length=10)
    Email = models.EmailField(max_length = 100, null = True, blank = True)
    

class AddPreferencesForm(ModelForm):
    class Meta:
        model=AddPreferences
        exclude = ['user_prefer']



