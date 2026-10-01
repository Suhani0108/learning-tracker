from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class SignupTests(TestCase):
    def test_signup_creates_user_and_logs_in(self):
        response = self.client.post(reverse("signup"), {
            "username": "newlearner",
            "password1": "a-long-Unusual-pass-42",
            "password2": "a-long-Unusual-pass-42",
        })
        self.assertRedirects(response, reverse("topics:list"))
        self.assertTrue(User.objects.filter(username="newlearner").exists())
        # The home page loads, which only works when logged in
        self.assertEqual(self.client.get(reverse("topics:list")).status_code, 200)

    def test_mismatched_passwords_show_error(self):
        response = self.client.post(reverse("signup"), {
            "username": "newlearner",
            "password1": "a-long-Unusual-pass-42",
            "password2": "something-else-42",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newlearner").exists())


class LoginLogoutTests(TestCase):
    def setUp(self):
        User.objects.create_user("alice", password="test-pass-123")

    def test_login_page_loads(self):
        self.assertEqual(self.client.get(reverse("login")).status_code, 200)

    def test_login_then_logout(self):
        response = self.client.post(reverse("login"), {
            "username": "alice",
            "password": "test-pass-123",
        })
        self.assertRedirects(response, reverse("topics:list"))

        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("login"))
