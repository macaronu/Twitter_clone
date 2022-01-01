import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User

class SignupForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'date_of_birth']

        current_year = datetime.datetime.now().year
        BirthYearChoices = range(1901, current_year + 1)
        widgets = { 'date_of_birth': forms.SelectDateWidget(years=BirthYearChoices)}
        error_messages = {'phone':{ 'invalid': 'Enter a valid phone number.' }}

class PasswordForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'date_of_birth', 'password1', 'password2']
        
        current_year = datetime.datetime.now().year
        birth_year_choices = range(1901, current_year + 1)
        widgets = { 'date_of_birth': forms.SelectDateWidget(years=birth_year_choices)}
