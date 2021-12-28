from django.forms import ModelForm
from django import forms
from .models import User
import datetime

class SignupForm(ModelForm):
    # overwrite the birth date field to add widgets
    current_year = datetime.datetime.now().year
    BirthYearChoices = range(1901, current_year + 1)
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=BirthYearChoices))
    
    class Meta:
        model = User
        exclude = ['password']

class PasswordForm(ModelForm):
    class Meta:
        model = User
        fields = ['password']
