from django.shortcuts import render

#index page for login, sign up and so on
def index_view(request):
    return render(request, "mytwitter/index.html")
