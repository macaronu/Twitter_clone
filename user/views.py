from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import SignupForm, PasswordForm
from django.views.generic import FormView

# Views for signing up

def signupPage(request):
    session_form_data1 = request.session.get('form_data1')
    form = SignupForm(session_form_data1)
    if request.method == "POST":
        form = SignupForm(request.POST)
        print (form.errors.as_data())
        if form.is_valid():
            request.session['form_data1'] = request.POST
            return redirect('user:create_password')

    return render(request, 'user/signup.html', {'form':form})

def passwordPage(request):
    session_form_data1 = request.session.get('form_data1')
    # session expired or invalid access
    if session_form_data1 is None:
        return redirect('user:signup')
    # default form
    form = PasswordForm(session_form_data1)
    # user inputs password
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            request.session['form_data2'] = request.POST
            return redirect('user:confirm')
    return render(request, 'user/password.html', {'form':form})

def signupConfirm(request):
    session_form_data2 = request.session.get('form_data2')
    if session_form_data2 is None:
        return redirect('user:signup')

    form = PasswordForm(session_form_data2)
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            del request.session['form_data1']
            del request.session['form_data2']
            form.save()
            return redirect('user:thanks')
    return render(request, 'user/signupConfirm.html', {'form':form})

def thanks(request):
    return render(request,'user/thanks.html')

