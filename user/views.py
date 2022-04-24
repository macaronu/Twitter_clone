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


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "user/profile/user_profile.html"
    permission_denied_message = "Oops! Seems like you haven't signed in yet."
    context_object_name = "page_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_user = get_object_or_404(CustomUser, id=self.kwargs["pk"])
        tweets = Tweet.objects.filter(user_id=page_user.id)
        request_user = self.request.user
        context["request_user"] = request_user
        context["tweets"] = tweets
        context["following"] = Follow.objects.filter(follower=page_user).count()
        context["follower"] = Follow.objects.filter(following=page_user).count()

        if page_user != request_user:
            is_following = Follow.objects.filter(follower=request_user).filter(
                following=page_user
            )
            context["is_following"] = True if is_following else False

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
    follower = CustomUser.objects.get(id=request.user.id)
    following = CustomUser.objects.get(id=kwargs["id"])
    if follower == following:
        messages.warning(request, "Haha, you can't follow yourself!")
    else:
        follow = Follow.objects.get_or_create(follower=follower, following=following)
    if follow:
        messages.success(
            request, "WooHoo! You have now followed {}".format(following.username)
        )
    else:
        messages.warning(
            request, "Seems like you're already following {}".format(following.username)
        )
    return redirect("user:user_profile", pk=following.id)


@login_required
def unfollow_view(request, **kwargs):
    follower = CustomUser.objects.get(id=request.user.id)
    following = CustomUser.objects.get(id=kwargs["id"])
    if follower == following:
        messages.warning(request, "Haha, you can't follow yourself!")
    else:
        unfollow = Follow.objects.get(follower=follower, following=following)
        unfollow.delete()
        messages.success(request, "You have unfollowed {}".format(following.username))
    return redirect("user:user_profile", pk=following.id)


class FollowerListView(ListView):
    model = Follow
    template_name = "user/follow/followers.html"

    def get_context_data(self, **kwargs):
        context = super(FollowerListView, self).get_context_data(**kwargs)
        page_user = get_object_or_404(CustomUser, username=self.kwargs["username"])
        request_user = self.request.user
        context["request_user"] = request_user
        context["page_user"] = page_user
        context["following"] = Follow.objects.filter(follower=page_user)
        context["followers"] = Follow.objects.filter(following=page_user)
        context["followed"] = Follow.objects.filter(follower=request_user)
        return context


class FollowingListView(ListView):
    model = Follow
    template_name = "user/follow/following.html"

    def get_context_data(self, **kwargs):
        context = super(FollowingListView, self).get_context_data(**kwargs)
        page_user = get_object_or_404(CustomUser, username=self.kwargs["username"])
        request_user = self.request.user
        context["request_user"] = request_user
        context["page_user"] = page_user
        context["following"] = Follow.objects.filter(follower=page_user)
        context["followers"] = Follow.objects.filter(following=page_user)
        context["followed"] = Follow.objects.filter(follower=request_user)
        return context
