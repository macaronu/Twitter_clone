from django.urls import path
from . import views


app_name = 'user'
urlpatterns = [
    path('', views.signup_view, name="signup"),
    path('password', views.password_view, name="create_password"),
    path('confirm', views.signup_confirm_view, name="confirm"),
    path('thanks', views.signup_thanks_view, name="thanks")
]
