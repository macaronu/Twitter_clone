from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm

from .models import User

# Views for signing up
def signupPage(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('signup:signup_detail', pk=post.pk)

    context = {'form':form}
    return render(request, 'signup/signup.html', context)

def signupDetail(request, pk):
    user = get_object_or_404(User, pk=pk)
    context = {'user':user}
    return render(request, 'signup/signupDetail.html', context)

"""
def passwordPage(request):
    form = PasswordForm()
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('signup:signup_detail', pk=post.pk)
    return HttpResponse("Enter password here")
"""