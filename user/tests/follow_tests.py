from django.contrib.messages import get_messages
from django.shortcuts import reverse
from django.test import TestCase

from ..models import CustomUser, Follow


class FollowTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="ポンデ", email="misdo@test.com", phone="", date_of_birth="1901-01-01"
        )
        self.user.set_password("12345")
        self.user.save()
        self.client.login(username="ポンデ", password="12345")

        self.user2 = CustomUser.objects.create(
            username="リング", email="misdo@test.com", phone="", date_of_birth="1901-01-01"
        )
        self.user2.set_password("12345")
        self.user2.save()

    def test_post_success(self):
        """
        POST: user/<int:pk>/follow/
        詳細: follow success
        効果: 302
        """
        url = reverse("user:follow", kwargs={"pk": self.user2.id})
        response = self.client.post(url)
        messages = [m.message for m in get_messages(response.wsgi_request)]

        self.assertTrue(
            Follow.objects.filter(follower=self.user, following=self.user2).exists()
        )
        self.assertRedirects(
            response, reverse("user:user_profile", kwargs={"pk": self.user2.id})
        )
        self.assertEqual(
            messages, [f"WooHoo! You have now followed {self.user2.username}"]
        )

    def test_post_with_non_existent_user(self):
        """
        POST: user/<int:pk>/follow/
        詳細: follow fails with non-existent user
        効果: 404
        """
        url = reverse("user:follow", kwargs={"pk": 5})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(
            Follow.objects.filter(follower=self.user, following=self.user2).exists()
        )

    def test_post_with_self(self):
        """
        POST: user/<int:pk>/follow/
        詳細: user cannot follow self
        効果: 302
        """
        url = reverse("user:follow", kwargs={"pk": self.user.id})
        response = self.client.post(url)
        messages = [m.message for m in get_messages(response.wsgi_request)]

        self.assertFalse(
            Follow.objects.filter(follower=self.user, following=self.user2).exists()
        )
        self.assertRedirects(
            response, reverse("user:user_profile", kwargs={"pk": self.user.id})
        )
        self.assertEqual(messages, ["Haha, you can't follow yourself!"])

    def test_post_with_already_following(self):
        """
        POST: user/<int:pk>/follow/
        詳細: already following
        効果: 302
        """
        Follow.objects.create(follower=self.user, following=self.user2)
        url = reverse("user:follow", kwargs={"pk": self.user2.id})
        response = self.client.post(url)
        messages = [m.message for m in get_messages(response.wsgi_request)]

        self.assertTrue(
            Follow.objects.filter(follower=self.user, following=self.user2).exists()
        )
        self.assertRedirects(
            response, reverse("user:user_profile", kwargs={"pk": self.user2.id})
        )
        self.assertEqual(
            messages, [f"Seems like you're already following {self.user2.username}"]
        )


class UnfollowTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="ポンデ", email="misdo@test.com", phone="", date_of_birth="1901-01-01"
        )
        self.user.set_password("12345")
        self.user.save()
        self.client.login(username="ポンデ", password="12345")

        self.user2 = CustomUser.objects.create(
            username="リング", email="misdo@test.com", phone="", date_of_birth="1901-01-01"
        )
        self.user2.set_password("12345")
        self.user2.save()
        Follow.objects.create(follower=self.user, following=self.user2)

    def test_post_success(self):
        """
        POST: user/<int:pk>/unfollow/
        詳細: unfollow success
        効果: 302
        """
        url = reverse("user:unfollow", kwargs={"pk": self.user2.id})
        response = self.client.post(url)
        messages = [m.message for m in get_messages(response.wsgi_request)]

        self.assertFalse(
            Follow.objects.filter(follower=self.user, following=self.user2).exists()
        )
        self.assertRedirects(
            response, reverse("user:user_profile", kwargs={"pk": self.user2.id})
        )
        self.assertEqual(messages, [f"You have unfollowed {self.user2.username}"])

    def test_post_with_non_existent_user(self):
        """
        POST: user/<int:pk>/unfollow/
        詳細: unfollow fails with non-existent user
        効果: 404
        """
        url = reverse("user:unfollow", kwargs={"pk": 5})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            Follow.objects.filter(follower=self.user, following=self.user2).exists()
        )

    def test_post_with_self(self):
        """
        POST: user/<int:pk>/unfollow/
        詳細: user cannot unfollow self
        効果: 302
        """
        url = reverse("user:unfollow", kwargs={"pk": self.user.id})
        response = self.client.post(url)
        messages = [m.message for m in get_messages(response.wsgi_request)]

        self.assertTrue(
            Follow.objects.filter(follower=self.user, following=self.user2).exists()
        )
        self.assertRedirects(
            response, reverse("user:user_profile", kwargs={"pk": self.user.id})
        )
        self.assertEqual(messages, ["Haha, you can't follow yourself!"])

    def test_post_with_already_following(self):
        """
        POST: user/<int:pk>/unfollow/
        詳細: already unfollowing
        効果: 302
        """
        Follow.objects.all().delete()
        url = reverse("user:unfollow", kwargs={"pk": self.user2.id})
        response = self.client.post(url)

        self.assertFalse(
            Follow.objects.filter(follower=self.user, following=self.user2).exists()
        )
        self.assertRedirects(
            response, reverse("user:user_profile", kwargs={"pk": self.user2.id})
        )


class FollowViewGetTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="ポンデ", email="misdo@test.com", phone="", date_of_birth="1901-01-01"
        )
        self.user.set_password("12345")
        self.user.save()
        self.client.login(username="ポンデ", password="12345")

    def test_get_followers_success(self):
        """
        POST: user/<int:pk>/followers/
        詳細: get success
        効果: 200
        """
        url = reverse("user:followers", kwargs={"pk": self.user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "user/follow/followers.html", "base_home.html"
        )

    def test_get_followers_with_non_existent_user(self):
        """
        POST: user/<int:pk>/followers/
        詳細: get fails with non-existent user
        効果: 404
        """
        url = reverse("user:followers", kwargs={"pk": 10})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(
            response, "user/follow/followers.html", "base_home.html"
        )

    def test_get_following_success(self):
        """
        POST: user/<int:pk>/following/
        詳細: get success
        効果: 200
        """
        url = reverse("user:following", kwargs={"pk": self.user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "user/follow/following.html", "base_home.html"
        )

    def test_get_following_with_non_existent_user(self):
        """
        POST: user/<int:pk>/following/
        詳細: get fails with non-existent user
        効果: 404
        """
        url = reverse("user:following", kwargs={"pk": 10})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(
            response, "user/follow/following.html", "base_home.html"
        )
