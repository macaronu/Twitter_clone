from django.core.files.images import ImageFile
from django.shortcuts import reverse
from django.test import TestCase

from .models import Tweet
from user.models import CustomUser


class CreateTweetTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="test", email="test@test.com", phone="", date_of_birth="1901-01-01"
        )
        self.user.set_password("12345")
        self.user.save()
        self.client.login(username="test", password="12345")
        self.url = reverse("tweets:tweet")

    def test_post_success(self):
        """
        POST: tweets/tweet/
        詳細: tweet success and redirects
        効果: 302
        """
        path = "./media/test/test_img.jpg"
        data = {"body": "今日の太陽はサンシャイン", "image": ImageFile(open(path, "rb"))}
        response = self.client.post(self.url, data)

        self.assertTrue(Tweet.objects.filter(user=self.user).exists())
        tweet = Tweet.objects.get(user=self.user)
        self.assertEqual(tweet.body, data["body"])
        self.assertTrue(tweet.image, data["image"])
        self.assertRedirects(response, reverse("user:home"))

    def test_post_fails_if_unauthorized(self):
        """
        POST: tweets/tweet/
        詳細: unauthorized access redirects to signin page
        効果: 302
        """
        path = "./media/test/test_img.jpg"
        data = {"body": "今日の太陽はサンシャイン", "image": ImageFile(open(path, "rb"))}
        self.client.logout()
        response = self.client.post(self.url, data)

        self.assertFalse(Tweet.objects.exists())
        self.assertRedirects(response, reverse("user:signin") + "?next=/tweets/tweet/")
        self.assertRaises(PermissionError)

    def test_post_fails_without_essential(self):
        """
        POST: tweets/tweet/
        詳細: body is not in data
        効果: 200
        """
        data = {}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Tweet.objects.exists())
        self.assertFormError(response, "form", "body", "This field is required.")

    def test_post_fails_with_empty_data(self):
        """
        POST: tweets/tweet/
        詳細: body is empty
        効果: 200
        """
        data = {"body": ""}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Tweet.objects.exists())
        self.assertFormError(response, "form", "body", "This field is required.")

    def test_post_fails_with_invalid_img_data(self):
        """
        POST: tweets/tweet/
        詳細: image is invalid
        効果: 200
        """
        path = "./media/test/test_txt.txt"
        data = {"body": "hi", "image": ImageFile(open(path, "rb"))}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Tweet.objects.exists())
        self.assertFormError(
            response,
            "form",
            "image",
            "Upload a valid image. The file you uploaded was either not an image or a corrupted image.",
        )


class EditTweetTests(TestCase):
    def setUp(self):
        user = CustomUser.objects.create(
            username="test", email="test@test.com", phone="", date_of_birth="1901-01-01"
        )
        user.set_password("12345")
        user.save()
        self.client.login(username="test", password="12345")
        path = "./media/test/test_img.jpg"
        self.tweet = Tweet.objects.create(
            user=user, body="test", image=ImageFile(open(path, "rb"))
        )
        self.url = reverse("tweets:tweet_edit", kwargs={"pk": self.tweet.id})

    def test_edit_success(self):
        """
        POST: tweets/<int:pk>/edit/
        詳細: edit success and redirects
        効果: 302
        """
        data = {"body": "今日の太陽はサンシャイン", "image": ""}
        response = self.client.post(self.url, data)
        self.tweet.refresh_from_db()

        self.assertEqual(self.tweet.body, data["body"])
        self.assertTrue(self.tweet.image, data["image"])
        self.assertRedirects(response, reverse("user:home"))

    def test_edit_fails_if_unauthorized(self):
        """
        POST: tweets/<int:pk>/edit/
        詳細: unauthorized access
        効果: 403
        """
        self.client.logout()
        user2 = CustomUser.objects.create(
            username="test2",
            email="test2@test.com",
            phone="",
            date_of_birth="1901-01-01",
        )
        user2.set_password("12345")
        user2.save()
        self.client.login(username="test2", password="12345")
        data = {"body": "今日の太陽はサンシャイン"}
        response = self.client.post(self.url, data)
        self.tweet.refresh_from_db()

        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(self.tweet.body, data["body"])
        self.assertRaises(PermissionError)

    def test_edit_fails_without_essential(self):
        """
        POST: tweets/<int:pk>/edit/
        詳細: body is not in data
        効果: 200
        """
        data = {}
        response = self.client.post(self.url, data)
        self.tweet.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.tweet.body, "test")
        self.assertFormError(response, "form", "body", "This field is required.")

    def test_edit_fails_with_empty_data(self):
        """
        POST: tweets/<int:pk>/edit/
        詳細: body is empty
        効果: 200
        """
        data = {"body": ""}
        response = self.client.post(self.url, data)
        self.tweet.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(self.tweet.body, data["body"])
        self.assertFormError(response, "form", "body", "This field is required.")

    def test_edit_fails_with_invalid_img_data(self):
        """
        POST: tweets/<int:pk>/edit/
        詳細: image is invalid
        効果: 200
        """
        path = "./media/test/test_txt.txt"
        data = {"body": "hi", "image": ImageFile(open(path, "rb"))}
        response = self.client.post(self.url, data)
        self.tweet.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(self.tweet.body, data["body"])
        self.assertNotEqual(self.tweet.image, data["image"])
        self.assertFormError(
            response,
            "form",
            "image",
            "Upload a valid image. The file you uploaded was either not an image or a corrupted image.",
        )

    def test_edit_fails_with_invalid_pk(self):
        """
        POST: tweets/<int:pk>/edit/
        詳細: pk is invalid
        効果: 404
        """
        self.url = reverse("tweets:tweet_edit", kwargs={"pk": "555"})
        data = {"body": "hi"}
        response = self.client.post(self.url, data)
        self.tweet.refresh_from_db()

        self.assertEqual(response.status_code, 404)
        self.assertNotEqual(self.tweet.body, data["body"])


class GetDetailTweetTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="test", email="test@test.com", phone="", date_of_birth="1901-01-01"
        )
        self.user.set_password("12345")
        self.user.save()
        self.client.login(username="test", password="12345")
        path = "./media/test/test_img.jpg"
        self.tweet = Tweet.objects.create(
            user=self.user, body="test", image=ImageFile(open(path, "rb"))
        )
        self.url = reverse(
            "tweets:tweet_detail",
            kwargs={"username": self.user.username, "pk": self.tweet.id},
        )

    def test_get_success(self):
        """
        GET: tweets/<str:username>/<int:pk>/
        詳細: get success
        効果: 200
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/tweet_detail.html")

    def test_get_success_by_other_users(self):
        """
        POST: tweets/<str:username>/<int:pk>/
        詳細: other users can access detail page
        効果: 200
        """
        self.client.logout()
        user2 = CustomUser.objects.create(
            username="test2",
            email="test2@test.com",
            phone="",
            date_of_birth="1901-01-01",
        )
        user2.set_password("12345")
        user2.save()
        self.client.login(username="test2", password="12345")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/tweet_detail.html")

    def test_get_fails_with_invalid_pk(self):
        """
        POST: tweets/<str:username>/<int:pk>/
        詳細: pk is invalid
        効果: 404
        """
        self.url = reverse(
            "tweets:tweet_detail", kwargs={"username": self.user.username, "pk": "555"}
        )
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)


class DeleteTweetTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="test", email="test@test.com", phone="", date_of_birth="1901-01-01"
        )
        self.user.set_password("12345")
        self.user.save()
        self.client.login(username="test", password="12345")
        path = "./media/test/test_img.jpg"
        self.tweet = Tweet.objects.create(
            user=self.user, body="test", image=ImageFile(open(path, "rb"))
        )
        self.url = reverse("tweets:tweet_delete", kwargs={"pk": self.tweet.id})

    def test_delete_success(self):
        """
        GET: tweets/<int:pk>/delete/
        詳細: delete success and redirects
        効果: 302
        """
        response = self.client.post(self.url)

        self.assertFalse(Tweet.objects.exists())
        self.assertRedirects(response, reverse("user:home"))

    def test_delete_fails_if_unauthorized(self):
        """
        POST: tweets/<int:pk>/delete/
        詳細: unauthorized access
        効果: 403
        """
        self.client.logout()
        user2 = CustomUser.objects.create(
            username="test2",
            email="test2@test.com",
            phone="",
            date_of_birth="1901-01-01",
        )
        user2.set_password("12345")
        user2.save()
        self.client.login(username="test2", password="12345")
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Tweet.objects.exists())
        self.assertRaises(PermissionError)

    def test_delete_fails_with_invalid_pk(self):
        """
        POST: tweets/<int:pk>/delete/
        詳細: pk is invalid
        効果: 404
        """
        self.url = reverse("tweets:tweet_delete", kwargs={"pk": "555"})
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Tweet.objects.exists())

    def test_delete_get_redirects(self):
        """
        GET: tweets/<int:pk>/delete/
        詳細: get delete view redirects to detail
        効果: 302
        """
        response = self.client.get(self.url)

        self.assertTrue(Tweet.objects.exists())
        self.assertRedirects(
            response,
            reverse(
                "tweets:tweet_detail",
                kwargs={"pk": self.tweet.id, "username": self.user.username},
            ),
        )
