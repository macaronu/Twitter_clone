from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


def directory_path(instance, filename):
    return f'profile/images/user_{instance.id}/{filename}'


class CustomUser(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(blank=False)
    phone = PhoneNumberField(blank=True)
    date_of_birth = models.DateField()
    profile_img = models.ImageField(upload_to=directory_path, blank=True)
    bio = models.TextField(max_length=280, null=True, blank=True)
    REQUIRED_FIELDS = ["date_of_birth"]
    
    @property
    def profile_img_url(self):
        if self.profile_img:
            return self.profile_img.url
        else:
            return "https://i.pinimg.com/550x/7a/95/ef/7a95ef5acbc87c558b3b4d7d0ddb3469.jpg"
