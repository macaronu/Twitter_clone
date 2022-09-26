from django.urls import path

from . import views


app_name = "tweets"
urlpatterns = [
    path("post/", views.TweetCreateView.as_view(), name="tweet"),
    path("<int:pk>/edit/", views.TweetEditView.as_view(), name="tweet_edit"),
    path("<int:pk>/delete/", views.TweetDeleteView.as_view(), name="tweet_delete"),
    path("<int:pk>/", views.TweetDetailView.as_view(), name="tweet_detail"),
    path("like/", views.like_view, name="like_tweet"),
]
