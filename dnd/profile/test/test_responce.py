from datetime import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class TestUrls(TestCase):

    def setUp(self) -> None:

        self.client = Client()

        self.user = get_user_model().objects.create_user(
            username="username",
            first_name="first_name",
            last_name="last_name",
            email="exemple@email.com",
            password="password",
            birth_date=datetime(1996, 5, 8, 0, 0),
            discord="User#0000",
            status_open_master=True,
            status_open_player=True,
        )

    def test_home(self):

        response = self.client.get(reverse("profile:home"))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='username', password='password')

        response = self.client.get(reverse("profile:home"))
        self.assertEqual(response.status_code, 200)

    def test_login(self):

        response = self.client.get(reverse("profile:login"))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):

        response = self.client.get(reverse("profile:logout"))
        self.assertEqual(response.status_code, 200)

    def test_register(self):

        response = self.client.get(reverse("profile:register"))
        self.assertEqual(response.status_code, 200)

    def test_account(self):

        response = self.client.get(reverse("profile:account"))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='username', password='password')

        response = self.client.get(reverse("profile:account"))
        self.assertEqual(response.status_code, 200)
