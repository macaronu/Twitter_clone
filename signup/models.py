from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinLengthValidator

# models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    phone = PhoneNumberField(blank=True)
    email = models.EmailField(max_length=254, blank=True)
    date_of_birth = models.DateField()
    password = models.CharField(max_length=50, validators=[MinLengthValidator(8, "Your password must be 8 characters or more")])
