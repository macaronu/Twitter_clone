import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

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


def user_directory_path(instance, filename):
    return os.path.join("user_" + str(instance.user.id), filename)


class Tweet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = models.TextField(max_length=280)
    image = models.ImageField(blank=True, null=True, upload_to=user_directory_path)
    likes = models.IntegerField(default=0)
    retweets = models.IntegerField(default=0)
    replies = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse(
            "user:tweet_detail",
            kwargs={"username": self.user.username, "tweet_id": self.id},
        )
