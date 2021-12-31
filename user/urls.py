from django.urls import path
from . import views


app_name = 'user'
urlpatterns = [
    path('', views.signupPage, name="signup"),
    path('password', views.passwordPage, name="create_password"),
    path('confirm', views.signupConfirm, name="confirm"),
    path('thanks', views.thanks, name="thanks")
]
