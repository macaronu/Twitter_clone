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
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from extra_views import UpdateWithInlinesView, InlineFormSetFactory, SuccessMessageMixin

from .models import CustomUser, Profile, Tweet
from .forms import SignupForm, PasswordForm


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
@login_required
def home_view(request):
    return render(request, "user/home.html")


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "user/profile/user_profile.html"
    permission_denied_message = "Oops! Seems like you haven't signed in yet."
    context_object_name = "page_user"


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


class HomeView(LoginRequiredMixin, ListView):
    model = Tweet
    template_name = "user/home.html"


class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "user/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        page_user = get_object_or_404(CustomUser, id=self.kwargs["pk"])
        tweets = Tweet.objects.filter(user_id=page_user.id)
        context["page_user"] = page_user
        context["tweets"] = tweets
        return context


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
