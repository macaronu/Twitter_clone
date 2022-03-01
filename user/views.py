from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

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
    return render(request, 'user/signup/signup.html', {'form':form})

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
    return render(request, 'user/signup/password.html', {'form':form})

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
    return render(request, 'user/signup/signupConfirm.html', {'form':form})

def signup_thanks_view(request):
    return render(request, 'user/signup/thanks.html')

# Views for signing in
class signin_view(LoginView):
    template_name = 'user/signin.html'
    next_page = 'user:home'

# Views for resetting password

class password_reset_view(PasswordResetView):
    template_name = "user/password_reset/password_reset_form.html"
    success_url = reverse_lazy('user:password_reset_done')
    email_template_name = "user/password_reset/password_reset_email.html"

class password_reset_done_view(PasswordResetDoneView):
    template_name = "user/password_reset/password_reset_done.html"

class password_reset_confirm_view(PasswordResetConfirmView):
    success_url = reverse_lazy('user:password_reset_complete')
    template_name = "user/password_reset/password_reset_confirm.html"

class password_reset_complete_view(PasswordResetCompleteView):
    template_name = "user/password_reset/password_reset_complete.html"

# Views for users
def home_view(request):
    return render(request, 'user/home.html')
