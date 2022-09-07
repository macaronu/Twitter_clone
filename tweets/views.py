from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy

from .models import Tweet


# Views for tweeting
class TweetView(LoginRequiredMixin, CreateView):
    model = Tweet
    template_name = "user/tweet.html"
    fields = ["user", "body", "image"]
    success_url = reverse_lazy("user:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TweetEditView(LoginRequiredMixin, UpdateView):
    model = Tweet
    template_name = "user/tweet_edit.html"
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
    template_name = "user/tweet_detail.html"


class HomeView(LoginRequiredMixin, ListView):
    model = Tweet
    template_name = "user/home.html"


class UserProfileView(LoginRequiredMixin, DetailView):
    model = "user.CustomUser"
    template_name = "user/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        page_user = get_object_or_404("user.CustomUser", id=self.kwargs["pk"])
        tweets = Tweet.objects.filter(user_id=page_user.id)
        context["page_user"] = page_user
        context["tweets"] = tweets
        return context
