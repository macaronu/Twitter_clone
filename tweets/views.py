from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
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


class TweetEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tweet
    template_name = "tweets/tweet_edit.html"
    fields = ["body", "image"]
    success_url = reverse_lazy("user:home")

    def test_func(self):
        tweet = self.get_object()
        if not (tweet.user == self.request.user):
            raise PermissionDenied
        return True


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet
    success_url = reverse_lazy("user:home")

    def get(self, **kwargs):
        return redirect("tweets:tweet_detail", pk=kwargs["pk"])

    def test_func(self):
        tweet = self.get_object()
        if not (tweet.user == self.request.user):
            raise PermissionDenied
        return True


class TweetDetailView(DetailView):
    queryset = Tweet.objects.select_related("user")
    template_name = "tweets/tweet_detail.html"
