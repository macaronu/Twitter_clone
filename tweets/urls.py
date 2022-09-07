from django.urls import path

from . import views


app_name = "tweets"
urlpatterns = [
    path("", views.TweetCreateView.as_view(), name="tweet"),
    path("<int:pk>/edit/", views.TweetEditView.as_view(), name="tweet_edit"),
    path("<int:pk>/delete/", views.TweetDeleteView.as_view(), name="tweet_delete"),
    path(
        "<str:username>/<int:pk>/", views.TweetDetailView.as_view(), name="tweet_detail"
    ),
]
