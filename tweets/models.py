from django.db import models


def directory_path(instance, filename):
    return f"tweets/images/user_{instance.user.id}/{filename}"


class Tweet(models.Model):
    user = models.ForeignKey(
        "user.CustomUser", on_delete=models.CASCADE, blank=True, related_name="tweets"
    )
    body = models.TextField(max_length=280)
    image = models.ImageField(blank=True, null=True, upload_to=directory_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.id)
