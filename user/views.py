from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView

from django.urls import reverse_lazy
from extra_views import UpdateWithInlinesView, InlineFormSetFactory, SuccessMessageMixin

from .models import CustomUser, Profile, Follow
from .forms import SignupForm, PasswordForm
from tweets.models import Tweet


# Views for signing up
def index_view(request):
    return render(request, "user/index.html")


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            request.session["info_form_data"] = request.POST
            return redirect("user:create_password")
    else:
        session_form_data = request.session.get("info_form_data")
        form = SignupForm(session_form_data)
    return render(request, "user/signup/signup.html", {"form": form})


def password_view(request):
    session_form_data = request.session.get("info_form_data")
    # session expired or invalid access
    if session_form_data is None:
        return redirect("user:signup")
    # user inputs password
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            request.session["password_form_data"] = request.POST
            return redirect("user:confirm")
    else:
        form = PasswordForm(session_form_data)
    return render(request, "user/signup/password.html", {"form": form})


def signup_confirm_view(request):
    session_form_data = request.session.get("password_form_data")
    if session_form_data is None:
        return redirect("user:signup")

    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            del request.session["info_form_data"]
            del request.session["password_form_data"]
            form.save()
            return redirect("user:thanks")
    else:
        form = PasswordForm(session_form_data)
    return render(request, "user/signup/signupConfirm.html", {"form": form})


def signup_thanks_view(request):
    return render(request, "user/signup/thanks.html")


# Views for signing in
class SigninView(LoginView):
    template_name = "user/signin.html"
    next_page = "user:home"


# Views for signing out
class SignoutView(LogoutView):
    template_name = "user/signedout.html"


# Views for resetting password
class PasswordResetView(PasswordResetView):
    template_name = "user/password_reset/password_reset_form.html"
    success_url = reverse_lazy("user:password_reset_done")
    email_template_name = "user/password_reset/password_reset_email.html"


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = "user/password_reset/password_reset_done.html"


class PasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("user:password_reset_complete")
    template_name = "user/password_reset/password_reset_confirm.html"


class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "user/password_reset/password_reset_complete.html"


# Views for users
class HomeView(LoginRequiredMixin, ListView):
    queryset = Tweet.objects.select_related("user")
    template_name = "user/home.html"
    permission_denied_message = "Oops! Seems like you haven't signed in yet."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["like_list"] = self.request.user.liked_tweets.values_list(
            "tweet", flat=True
        )
        return context


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "user/profile/user_profile.html"
    permission_denied_message = "Oops! Seems like you haven't signed in yet."
    context_object_name = "page_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_user = self.get_object()
        request_user = self.request.user
        context["tweets"] = page_user.tweets.all()
        context["like_list"] = request_user.liked_tweets.all()
        context["following"] = page_user.followers.count()
        context["followers"] = page_user.following.count()
        if page_user != request_user:
            is_following = page_user.followers.filter(follower=request_user).exists()
            context["is_following"] = is_following

        return context


class ProfileInline(InlineFormSetFactory):
    model = Profile
    fields = ["profile_img", "bio"]
    factory_kwargs = {"can_delete": False}


class EditProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateWithInlinesView):
    model = CustomUser
    inlines = [ProfileInline]
    fields = ["username"]
    template_name = "user/profile/edit_profile.html"
    permission_denied_message = "Oops! Seems like you haven't signed in yet."
    success_message = "Profile Updated!"

    # Redirect to user's profile page with kwargs on success
    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse_lazy("user:user_profile", kwargs={"pk": pk})

    def user_passes_test(self, request):
        if request.user.is_authenticated:
            self.object = self.get_object()
            return self.object == request.user
        return False

    # Users cannot access other people's edit pages
    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect("user:home")
        return super().dispatch(request, *args, **kwargs)


# Views for following
@login_required
def follow_view(request, **kwargs):
    follower = get_object_or_404(CustomUser, id=request.user.id)
    following = get_object_or_404(CustomUser, id=kwargs["pk"])
    if follower == following:
        messages.warning(request, "Haha, you can't follow yourself!")
    elif Follow.objects.filter(follower=follower, following=following).exists():
        messages.warning(
            request, f"Seems like you're already following {following.username}"
        )
    else:
        Follow.objects.create(follower=follower, following=following)
        messages.success(request, f"WooHoo! You have now followed {following.username}")
    return redirect("user:user_profile", pk=following.id)


@login_required
def unfollow_view(request, **kwargs):
    follower = get_object_or_404(CustomUser, id=request.user.id)
    following = get_object_or_404(CustomUser, id=kwargs["pk"])
    if follower == following:
        messages.warning(request, "Haha, you can't follow yourself!")
    elif not Follow.objects.filter(follower=follower, following=following).exists():
        pass
    else:
        unfollow = get_object_or_404(Follow, follower=follower, following=following)
        unfollow.delete()
        messages.success(request, f"You have unfollowed {following.username}")
    return redirect("user:user_profile", pk=following.id)


class FollowerListView(LoginRequiredMixin, ListView):
    model = Follow
    template_name = "user/follow/followers.html"

    def get_context_data(self, **kwargs):
        context = super(FollowerListView, self).get_context_data(**kwargs)
        page_user = get_object_or_404(CustomUser, pk=self.kwargs["pk"])
        followers_list = Follow.objects.select_related("following").filter(
            following=page_user
        )
        context["page_user"] = page_user
        context["followers_list"] = followers_list
        return context


class FollowingListView(LoginRequiredMixin, ListView):
    model = Follow
    template_name = "user/follow/following.html"

    def get_context_data(self, **kwargs):
        context = super(FollowingListView, self).get_context_data(**kwargs)
        page_user = get_object_or_404(CustomUser, pk=self.kwargs["pk"])
        following_list = Follow.objects.select_related("follower").filter(
            follower=page_user
        )
        context["page_user"] = page_user
        context["following_list"] = following_list
        return context
