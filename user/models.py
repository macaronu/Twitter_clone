from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    email = models.EmailField(blank=False)
    phone = PhoneNumberField(blank=True)
    date_of_birth = models.DateField()
    REQUIRED_FIELDS = ["date_of_birth"]
