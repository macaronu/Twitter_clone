from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy

from .models import Tweet, TweetLike


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

    def get(self, request, **kwargs):
        return redirect("tweets:tweet_detail", pk=kwargs["pk"])

    def test_func(self):
        tweet = self.get_object()
        if not (tweet.user == self.request.user):
            raise PermissionDenied
        return True


class TweetDetailView(LoginRequiredMixin, DetailView):
    queryset = Tweet.objects.select_related("user")
    template_name = "tweets/tweet_detail.html"

    def get_context_data(self, **kwargs):
        tweet = self.get_object()
        context = super().get_context_data(**kwargs)
        context["liked"] = TweetLike.objects.filter(
            tweet=tweet, liked_by=self.request.user
        ).exists()
        return context


# Views for liking
@login_required(login_url="user:signup")
def like_view(request, **kwargs):
    tweetid = request.POST.get("tweetid")
    tweet = get_object_or_404(Tweet, id=tweetid)
    like = TweetLike.objects.filter(tweet=tweet, liked_by=request.user)
    context = {"user": request.user.username, "tweetid": tweetid}
    if like.exists():
        like.delete()
        context["method"] = "delete"
    else:
        like.create(tweet=tweet, liked_by=request.user)
        context["method"] = "create"
    context["like_count"] = tweet.likes.count()
    return JsonResponse(context)
