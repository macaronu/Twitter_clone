import datetime

from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, SelectDateWidget, Textarea

from .models import CustomUser, Tweet


class SignupForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone", "date_of_birth"]

        current_year = datetime.datetime.now().year
        BirthYearChoices = range(1901, current_year + 1)
        widgets = {"date_of_birth": SelectDateWidget(years=BirthYearChoices)}
        error_messages = {"phone": {"invalid": "Enter a valid phone number."}}


class PasswordForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "phone",
            "date_of_birth",
            "password1",
            "password2",
        ]

        current_year = datetime.datetime.now().year
        birth_year_choices = range(1901, current_year + 1)
        widgets = {"date_of_birth": SelectDateWidget(years=birth_year_choices)}


class TweetForm(ModelForm):
    class Meta:
        model = Tweet
        fields = ["user", "body", "image"]
        widgets = {"body": Textarea(attrs={"placeholder": "What's Happening?"})}
