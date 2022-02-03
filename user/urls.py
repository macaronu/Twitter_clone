from django.urls import path

from . import views


app_name = 'user'
urlpatterns = [
    path('', views.index_view, name="index"),
    path('signup/', views.signup_view, name="signup"),
    path('signup_password/', views.password_view, name="create_password"),
    path('signup_confirm/', views.signup_confirm_view, name="confirm"),
    path('thanks/', views.signup_thanks_view, name="thanks"),
    path('signin/', views.signin_view.as_view(), name="signin"),
    path('password_reset/', views.password_reset_view.as_view(), name="reset_password"),
    path('password_reset/sent/', views.password_reset_done_view.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm_view.as_view(), name="password_reset_confirm"),
    path('password_reset/complete/', views.password_reset_complete_view.as_view(), name="password_reset_complete"),
    path('home/', views.home_view, name="home")
]
