from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


def directory_path(instance, filename):
    return f"profile/images/user_{instance.user.id}/{filename}"


class CustomUser(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(blank=False)
    phone = PhoneNumberField(blank=True)
    date_of_birth = models.DateField()
    REQUIRED_FIELDS = ["date_of_birth"]


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    profile_img = models.ImageField(upload_to=directory_path, blank=True)
    bio = models.TextField(max_length=280, null=True, blank=True)

    @property
    def profile_img_url(self):
        if self.profile_img:
            return self.profile_img.url
        else:
            return "https://i.pinimg.com/550x/7a/95/ef/7a95ef5acbc87c558b3b4d7d0ddb3469.jpg"
