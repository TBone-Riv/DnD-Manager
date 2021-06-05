from datetime import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve
from dnd.game.models import (
    Campaign,
    Character,
    Session
)
from dnd.game.views import (
    # CAMPAIGN
    CampaignListView,
    CampaignCreateView,
    CampaignUpdateView,
    CampaignDetailView,
    # CHARACTER
    CharacterListView,
    CharacterCampaignListView,
    CharacterCreateView,
    CharacterUpdateView,
    CharacterDetailView,
    # SESSION
    SessionListView,
    SessionCampaignListView,
    SessionCharacterListView,
    SessionCreateView,
    SessionUpdateView,
    SessionDetailView,
    SessionStatusUpdateView
)


class TestCampaign(TestCase):

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

    def test_list(self):
        url = reverse("game:list-campaign", kwargs={'user_name': "username"})
        self.assertEqual(resolve(url).func.__name__,
                         CampaignListView.as_view().__name__)

    def test_create(self):
        url = reverse("game:new-campaign")
        self.assertEqual(resolve(url).func.__name__,
                         CampaignCreateView.as_view().__name__)

    def test_update(self):
        url = reverse("game:my-campaign", kwargs={'pk': self.campaign.id})
        self.assertEqual(resolve(url).func.__name__,
                         CampaignUpdateView.as_view().__name__)

    def test_detail(self):
        url = reverse("game:campaign", kwargs={'pk': self.campaign.id})
        self.assertEqual(resolve(url).func.__name__,
                         CampaignDetailView.as_view().__name__)


class TestCharacter(TestCase):

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

    def test_list(self):
        url = reverse("game:list-character", kwargs={'user_name': "username"})
        self.assertEqual(resolve(url).func.__name__,
                         CharacterListView.as_view().__name__)

    def test_list_campaign(self):
        url = reverse("game:list-campaign-character",
                      kwargs={'pk': self.campaign.id})
        self.assertEqual(resolve(url).func.__name__,
                         CharacterCampaignListView.as_view().__name__)

    def test_create(self):
        url = reverse("game:new-character")
        self.assertEqual(resolve(url).func.__name__,
                         CharacterCreateView.as_view().__name__)

    def test_update(self):
        url = reverse("game:my-character", kwargs={'pk': self.character.id})
        self.assertEqual(resolve(url).func.__name__,
                         CharacterUpdateView.as_view().__name__)

    def test_detail(self):
        url = reverse("game:character", kwargs={'pk': self.character.id})
        self.assertEqual(resolve(url).func.__name__,
                         CharacterDetailView.as_view().__name__)


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

    def test_list(self):
        url = reverse("game:list-session", kwargs={'user_name': "username"})
        self.assertEqual(resolve(url).func.__name__,
                         SessionListView.as_view().__name__)

    def test_list_campaign(self):
        url = reverse("game:list-campaign-session",
                      kwargs={'pk': self.campaign.id})
        self.assertEqual(resolve(url).func.__name__,
                         SessionCampaignListView.as_view().__name__)

    def test_list_character(self):
        url = reverse("game:list-character-session",
                      kwargs={'pk': self.character.id})
        self.assertEqual(resolve(url).func.__name__,
                         SessionCharacterListView.as_view().__name__)

    def test_create(self):
        url = reverse("game:new-session", kwargs={'pk': self.campaign.id})
        self.assertEqual(resolve(url).func.__name__,
                         SessionCreateView.as_view().__name__)

    def test_update(self):
        url = reverse("game:my-session", kwargs={'pk': self.session.id})
        self.assertEqual(resolve(url).func.__name__,
                         SessionUpdateView.as_view().__name__)

    def test_detail(self):
        url = reverse("game:session", kwargs={'pk': self.session.id})
        self.assertEqual(resolve(url).func.__name__,
                         SessionDetailView.as_view().__name__)

    def test_vote(self):
        url = reverse("game:vote-session", kwargs={'pk': self.session.id})
        self.assertEqual(resolve(url).func.__name__,
                         SessionStatusUpdateView.as_view().__name__)
