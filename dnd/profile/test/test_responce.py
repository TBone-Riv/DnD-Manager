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

        self.assertEqual(response.status_code, 302) # falow true + asser ulr de redirection

        self.client.login(username='username', password='password')

        response = self.client.get(reverse("profile:home"))
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_login(self):

        response = self.client.get(reverse("profile:login"))
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):

        response = self.client.get(reverse("profile:logout"))
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_register(self):

        response = self.client.get(reverse("profile:register"))
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_account(self):

        response = self.client.get(reverse("profile:account"))

        self.assertEqual(response.status_code, 302)

        self.client.login(username='username', password='password')

        response = self.client.get(reverse("profile:account"))
        print(response.status_code)
        self.assertEqual(response.status_code, 200)
