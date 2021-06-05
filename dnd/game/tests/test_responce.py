from datetime import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from dnd.game.models import (
    Campaign,
    Character,
    Session
)


class TestCampaign(TestCase):

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

        self.campaign = Campaign.objects.create(
            title="campaign1",
            max_player=5,
            master=self.user,
            creator=self.user
        )

        self.client.login(username='username', password='password')

        self.user2 = get_user_model().objects.create_user(
            username="username2",
            first_name="first_name",
            last_name="last_name",
            email="exemple@email.com",
            password="password",
            birth_date=datetime(1996, 5, 8, 0, 0),
            discord="User#0000",
            status_open_master=True,
            status_open_player=True,
        )

    def test_list(self):
        url = reverse("game:list-campaign", kwargs={'user_name': "username"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        url = reverse("game:new-campaign")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        url = reverse("game:my-campaign", kwargs={'pk': self.campaign.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_redirect(self):

        self.client.logout()
        self.client.login(username='username2', password='password')

        url = reverse("game:my-campaign", kwargs={'pk': self.campaign.id})
        url_detail = reverse("game:campaign", kwargs={'pk': self.campaign.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, url_detail)

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        url = reverse("game:campaign", kwargs={'pk': self.campaign.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestCharacter(TestCase):

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

        self.campaign = Campaign.objects.create(
            title="campaign1",
            max_player=5,
            master=self.user,
            creator=self.user
        )

        self.character = Character.objects.create(
            name="character1",
            character_class="class",
            character_race="race",
            character_level=10,
            creator=self.user,
            in_campaign=self.campaign,
        )

        self.client.login(username='username', password='password')

        self.user2 = get_user_model().objects.create_user(
            username="username2",
            first_name="first_name",
            last_name="last_name",
            email="exemple@email.com",
            password="password",
            birth_date=datetime(1996, 5, 8, 0, 0),
            discord="User#0000",
            status_open_master=True,
            status_open_player=True,
        )

    def test_list(self):
        url = reverse("game:list-character", kwargs={'user_name': "username"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        url = reverse("game:new-character")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        url = reverse("game:my-character", kwargs={'pk': self.character.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_redirect(self):

        self.client.logout()
        self.client.login(username='username2', password='password')

        url = reverse("game:my-character", kwargs={'pk': self.character.id})
        url_detail = reverse("game:character",
                             kwargs={'pk': self.character.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, url_detail)

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        url = reverse("game:character", kwargs={'pk': self.character.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestSession(TestCase):

    def setUp(self) -> None:

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

        self.campaign = Campaign.objects.create(
            title="campaign1",
            max_player=5,
            master=self.user,
            creator=self.user
        )

        self.character = Character.objects.create(
            name="character1",
            character_class="class",
            character_race="race",
            character_level=10,
            creator=self.user,
            in_campaign=self.campaign,
        )

        self.session = Session.objects.create(
            title="session1",
            date=datetime(2030, 5, 8, 0, 0),
            for_campaign=self.campaign,
            creator=self.user
        )

        self.client.login(username='username', password='password')

    def test_list(self):
        url = reverse("game:list-session", kwargs={'user_name': "username"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_campaign(self):
        url = reverse("game:list-campaign-session",
                      kwargs={'pk': self.campaign.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_character(self):
        url = reverse("game:list-character-session",
                      kwargs={'pk': self.character.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        url = reverse("game:new-session", kwargs={'pk': self.campaign.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        url = reverse("game:my-session", kwargs={'pk': self.session.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        url = reverse("game:session", kwargs={'pk': self.session.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_vote(self):
        url = reverse("game:vote-session", kwargs={'pk': self.session.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
