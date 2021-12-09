from django.urls import path
from . import views


app_name = 'signup'
urlpatterns = [
    path('', views.signupPage, name="signup"),
    path('<int:pk>', views.signupDetail, name="signup_detail"),
    #path('password', views.passwordPage, name="create_password")
]
