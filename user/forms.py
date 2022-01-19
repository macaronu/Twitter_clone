import datetime

from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, SelectDateWidget

from .models import CustomUser


class SignupForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'date_of_birth']

        current_year = datetime.datetime.now().year
        BirthYearChoices = range(1901, current_year + 1)
        widgets = { 'date_of_birth': SelectDateWidget(years=BirthYearChoices)}
        error_messages = {'phone':{ 'invalid': 'Enter a valid phone number.' }}

class PasswordForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'date_of_birth', 'password1', 'password2']
        
        current_year = datetime.datetime.now().year
        birth_year_choices = range(1901, current_year + 1)
        widgets = { 'date_of_birth': SelectDateWidget(years=birth_year_choices)}
