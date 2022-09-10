from django.urls import path

from . import views


app_name = "user"
urlpatterns = [
    path("", views.index_view, name="index"),
    path("signup/", views.signup_view, name="signup"),
    path("signup_password/", views.password_view, name="create_password"),
    path("signup_confirm/", views.signup_confirm_view, name="confirm"),
    path("thanks/", views.signup_thanks_view, name="thanks"),
    path("signin/", views.SigninView.as_view(), name="signin"),
    path("signout/", views.SignoutView.as_view(), name="signout"),
    path("password_reset/", views.PasswordResetView.as_view(), name="reset_password"),
    path(
        "password_reset/sent/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password_reset/complete/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("home/", views.HomeView.as_view(), name="home"),
    path("<int:pk>/", views.ProfileView.as_view(), name="user_profile"),
    path("<int:pk>/edit/", views.EditProfileView.as_view(), name="edit_profile"),
    path("<int:id>/follow", views.follow_view, name="follow"),
    path("<int:id>/unfollow", views.unfollow_view, name="unfollow"),
    path(
        "<slug:username>/followers", views.FollowerListView.as_view(), name="followers"
    ),
    path(
        "<slug:username>/following", views.FollowingListView.as_view(), name="following"
    ),
]
