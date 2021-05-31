from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class TestPasswordChange(StaticLiveServerTestCase):

    def setUp(self):

        self.browser = webdriver.Edge('dnd/base/tests/msedgedriver.exe')

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

    def tearDown(self):
        self.browser.close()

    def test_campaign(self):

        url_login = self.live_server_url + reverse("profile:login")
        url_start = self.live_server_url + reverse("game:new-campaign")

        self.browser.get(url_start)

        self.assertEqual(
            self.browser.current_url,
            url_login + '?next=' + reverse("game:new-campaign")
        )

        username_box = self.browser.find_element_by_name("username")

        username_box.send_keys("username")

        password_box = self.browser.find_element_by_name("password")

        password_box.send_keys("password")

        password_box.send_keys(Keys.ENTER)

        self.assertEqual(
            self.browser.current_url,
            url_start
        )

        title_box = self.browser.find_element_by_name("title")

        title_box.send_keys("title")

        details_box = self.browser.find_element_by_name("details")

        details_box.send_keys("details")

        max_player_box = self.browser.find_element_by_name("max_player")

        max_player_box.send_keys("2")

        max_player_box.send_keys(Keys.ENTER)

        time.sleep(10)

        self.assertEqual(
            self.browser.current_url.split('/')[-1],
            'update'
        )
