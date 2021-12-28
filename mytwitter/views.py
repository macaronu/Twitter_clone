from django.shortcuts import render, HttpResponse

#index page for login, sign up and so on
def index(request):
    return render(request, "mytwitter/index.html")