from django.db import models
from django.utils.encoding import smart_unicode
from django.contrib.auth.models import User
from django.forms import ModelForm

class Bug(models.Model):
    #getting the user 
    reporter= models.ForeignKey(User)
    Bug = models.TextField(max_length=250)

class BugForm(ModelForm):
    class Meta:
        model=Bug
        exclude = ['reporter']



