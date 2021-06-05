from django.test import SimpleTestCase
from django.urls import reverse, resolve
from dnd.profile.views import (
    HomeView,
    CustomLoginView,
    CustomLogoutView,
    CreateCustomUserView,
    UpdateCustomUserView
)


class TestUrls(SimpleTestCase):

    def test_home(self):
        url = reverse("profile:home")
        self.assertEqual(resolve(url).func.__name__,
                         HomeView.as_view().__name__)

    def test_login(self):
        url = reverse("profile:login")
        self.assertEqual(resolve(url).func.__name__,
                         CustomLoginView.as_view().__name__)

    def test_logout(self):
        url = reverse("profile:logout")
        self.assertEqual(resolve(url).func.__name__,
                         CustomLogoutView.as_view().__name__)

    def test_register(self):
        url = reverse("profile:register")
        self.assertEqual(resolve(url).func.__name__,
                         CreateCustomUserView.as_view().__name__)

    def test_account(self):
        url = reverse("profile:account")
        self.assertEqual(resolve(url).func.__name__,
                         UpdateCustomUserView.as_view().__name__)
