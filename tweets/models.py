from django.db import models
from django.urls import reverse


def directory_path(instance, filename):
    return f"profile/images/user_{instance.user.id}/{filename}"


class Tweet(models.Model):
    user = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = models.TextField(max_length=280)
    image = models.ImageField(blank=True, null=True, upload_to=directory_path)
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
