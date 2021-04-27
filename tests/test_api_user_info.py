from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from osp.utils.zulip_api import get_self_zulip_id

User = get_user_model()


class UserInfoTests(APITestCase):
    def setUp(self):

        # Needed for token auths
        self.client = APIClient()

        # Register
        self.register_data = {
            "username": "testuser1",
            "email": "testuser1@gmail.com",
            "password": "hello",
            "confirm_password": "hello",
        }
        test_user = User(username=self.register_data["username"], email=self.register_data["email"], is_active=True)
        test_user.set_password(self.register_data["password"])
        test_user.save()

        # Login and get real token
        login_data = {"username": self.register_data["username"], "password": self.register_data["password"]}
        response = self.client.post(
            "http://localhost:8000/api/token_auth/token/",
            login_data,
            format="json",
            headers={"Content-Type": "application/json"},
        )
        self.access_token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

        self.zulip_id = get_self_zulip_id()

    def test_get_user_info_successfully_empty(self):

        response = self.client.get("http://localhost:8000/api/info/", format="json")
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_user_info_successfully(self):

        body = {"name": "Test User 1 Full Name", "user_type": "admin", "zulip_id": self.zulip_id}
        response = self.client.post("http://localhost:8000/api/info/", body, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], body["name"])
        self.assertEqual(response.data["user_type"], body["user_type"])
        self.assertEqual(response.data["zulip_id"], body["zulip_id"])
        self.assertEqual(response.data["user"]["email"], self.register_data["email"])
        self.assertEqual(response.data["user"]["username"], self.register_data["username"])

    def test_get_user_info_successfully(self):

        body = {"name": "Test User 1 Full Name", "user_type": "admin", "zulip_id": self.zulip_id}
        response = self.client.post("http://localhost:8000/api/info/", body, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data, [])

        response = self.client.get("http://localhost:8000/api/info/", format="json")
        response.data = response.data[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, [])
        self.assertEqual(response.data["name"], body["name"])
        self.assertEqual(response.data["user_type"], body["user_type"])
        self.assertEqual(response.data["zulip_id"], body["zulip_id"])
        self.assertEqual(response.data["user"]["email"], self.register_data["email"])
        self.assertEqual(response.data["user"]["username"], self.register_data["username"])

    def test_api_wrong_token(self):

        self.client.credentials()
        response = self.client.get("http://localhost:8000/api/info/", format="json")
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")
        self.assertEqual(response.status_code, 403)

    def test_multiple_post_user_info(self):

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        body = {"name": "Test User 1 Full Name", "user_type": "admin", "zulip_id": self.zulip_id}
        for _ in range(2):
            response = self.client.post("http://localhost:8000/api/info/", body, format="json")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
