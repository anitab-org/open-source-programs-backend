import json

import responses
from allauth.socialaccount.models import SocialApp
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class TestGitHubAuth(TestCase):
    """
    Tests for Github Authentication.
    """

    def setUp(self):
        self.client = APIClient()
        self.github_login_url = reverse("github_login")
        self.payload = {"code": "123456"}
        social_app = SocialApp.objects.create(
            provider="github",
            name="Github",
            client_id="123123123",
            secret="321321321",
        )
        site = Site.objects.get_current()
        social_app.sites.add(site)

    @responses.activate
    def test_github_auth(self):
        """
        Testing GitHub Auth Registration and Login.
        """
        # fake responses to mock GitHub API call
        self.__add_github_responses()

        users_count = get_user_model().objects.all().count()

        response = self.client.post(self.github_login_url, data=self.payload, format="json")

        self.assertEquals(response.status_code, 200)
        # assertion to check new user is created.
        self.assertEquals(get_user_model().objects.all().count(), users_count + 1)

        # Below two assertions are added to check REST_USE_JWT is True or not.
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

        # Assertion to check second request will not create a new user
        response = self.client.post(self.github_login_url, data=self.payload, format="json")
        self.assertEquals(get_user_model().objects.all().count(), users_count + 1)

    def __add_github_responses(self):
        """
        Private methods to add responses for different GitHub API Calls.
        """

        responses.add(
            responses.POST,
            "https://github.com/login/oauth/access_token",
            body=json.dumps({"access_token": "access_token"}),
            status=200,
            content_type="application/json",
        )

        responses.add(
            responses.GET,
            "https://api.github.com/user",
            body=json.dumps({"id": "123456", "login": "TestUser", "name": "Test User", "type": "User"}),
            status=200,
            content_type="application/json",
        )
