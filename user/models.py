from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField()
    phone = PhoneNumberField(blank=True)
    date_of_birth = models.DateField()
    REQUIRED_FIELDS = ["date_of_birth"]
