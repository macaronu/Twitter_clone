from django.forms import ModelForm, Textarea

from .models import Tweet


class TweetForm(ModelForm):
    class Meta:
        model = Tweet
        fields = ["user", "body", "image"]
        widgets = {"body": Textarea(attrs={"placeholder": "What's Happening?"})}
