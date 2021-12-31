from django.shortcuts import render, redirect
from .forms import SignupForm, PasswordForm

# Views for signing up

def signup_view(request):
    session_form_data = request.session.get('info_form_data')
    form = SignupForm(session_form_data)
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            request.session['info_form_data'] = request.POST
            return redirect('user:create_password')
    return render(request, 'user/signup.html', {'form':form})

def password_view(request):
    session_form_data = request.session.get('info_form_data')
    # session expired or invalid access
    if session_form_data is None:
        return redirect('user:signup')
    # default form
    form = PasswordForm(session_form_data)
    # user inputs password
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            request.session['password_form_data'] = request.POST
            return redirect('user:confirm')
    return render(request, 'user/password.html', {'form':form})

def signup_confirm_view(request):
    session_form_data = request.session.get('password_form_data')
    if session_form_data is None:
        return redirect('user:signup')
    
    form = PasswordForm(session_form_data)
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            del request.session['info_form_data']
            del request.session['password_form_data']
            form.save()
            return redirect('user:thanks')
    return render(request, 'user/signupConfirm.html', {'form':form})

def signup_thanks_view(request):
    return render(request,'user/thanks.html')
