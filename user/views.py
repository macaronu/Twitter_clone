from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic import DetailView, UpdateView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import CustomUser
from .forms import SignupForm, PasswordForm


# Views for signing up
def index_view(request):
    return render(request, 'user/index.html')


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            request.session['info_form_data'] = request.POST
            return redirect('user:create_password')
    else:
        session_form_data = request.session.get('info_form_data')
        form = SignupForm(session_form_data)
    return render(request, 'user/signup/signup.html', {'form': form})


def password_view(request):
    session_form_data = request.session.get('info_form_data')
    # session expired or invalid access
    if session_form_data is None:
        return redirect('user:signup')
    # user inputs password
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            request.session['password_form_data'] = request.POST
            return redirect('user:confirm')
    else:
        form = PasswordForm(session_form_data)
    return render(request, 'user/signup/password.html', {'form': form})


def signup_confirm_view(request):
    session_form_data = request.session.get('password_form_data')
    if session_form_data is None:
        return redirect('user:signup')

    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            del request.session['info_form_data']
            del request.session['password_form_data']
            form.save()
            return redirect('user:thanks')
    else:
        form = PasswordForm(session_form_data)
    return render(request, 'user/signup/signupConfirm.html', {'form': form})


def signup_thanks_view(request):
    return render(request, 'user/signup/thanks.html')


# Views for signing in
class SigninView(LoginView):
    template_name = 'user/signin.html'
    next_page = 'user:home'


# Views for signing out
class SignoutView(LogoutView):
    template_name = 'user/signedout.html'


# Views for resetting password
class PasswordResetView(PasswordResetView):
    template_name = "user/password_reset/password_reset_form.html"
    success_url = reverse_lazy('user:password_reset_done')
    email_template_name = "user/password_reset/password_reset_email.html"


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = "user/password_reset/password_reset_done.html"


class PasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('user:password_reset_complete')
    template_name = "user/password_reset/password_reset_confirm.html"


class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "user/password_reset/password_reset_complete.html"


# Views for users
def user_unauthenticated_view(request):
    return render(request, 'user/user_unauthenticated.html')


@login_required
def home_view(request):
    return render(request, 'user/home.html')


class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'user/profile/user_profile.html'
    permission_denied_message = "Oops! Seems like you haven't signed in yet."
    context_object_name = 'page_user'


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'user/profile/edit_profile.html'
    fields = ['username', 'profile_img', 'bio']
    permission_denied_message = "Oops! Seems like you haven't signed in yet."

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
            return redirect('user:home')
        return super().dispatch(request, *args, **kwargs)
