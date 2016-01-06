from django import forms
from .models import ShowMap

class ShowMapForm(forms.ModelForm):
    class Meta:
        model=ShowMap