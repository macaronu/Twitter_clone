from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy

from .models import Tweet


# Views for tweeting
class TweetCreateView(LoginRequiredMixin, CreateView):
    model = Tweet
    template_name = "tweets/tweet.html"
    fields = ["user", "body", "image"]
    success_url = reverse_lazy("user:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TweetEditView(LoginRequiredMixin, UpdateView):
    model = Tweet
    template_name = "tweets/tweet_edit.html"
    fields = ["body", "image"]
    success_url = reverse_lazy("user:home")

    def dispatch(self, request, *args, **kwargs):
        handler = super().dispatch(request, *args, **kwargs)
        user = request.user
        tweet = self.get_object()
        if not (tweet.user == user):
            raise PermissionDenied
        return handler


class TweetDeleteView(LoginRequiredMixin, DeleteView):
    model = Tweet
    success_url = reverse_lazy("user:home")


class TweetDetailView(DetailView):
    model = Tweet
    template_name = "tweets/tweet_detail.html"
