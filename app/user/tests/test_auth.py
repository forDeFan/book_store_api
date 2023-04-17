from core.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


class TestAuthCase(TestCase):
    """Test class for user authentication."""

    LOGIN_FOR_TOKEN_URL = reverse("user:login")
    REFRESH_TOKEN_URL = reverse("user:refresh")
    LOGOUT_TO_BLACKLIST_REFRESH_TOKEN_URL = reverse("user:logout")

    EMAIL = "test@example.com"
    PASSWORD = "test_pass"
    NAME = "test_name"

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email=self.EMAIL, password=self.PASSWORD, name=self.NAME
        )

    def test_token_created_for_user(self):
        payload = {"email": self.EMAIL, "password": self.PASSWORD}

        res = self.client.post(self.LOGIN_FOR_TOKEN_URL, payload)

        self.assertIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_401_when_bad_credentials_for_token(self):
        payload = {"email": self.EMAIL, "password": "bad_password"}

        res = self.client.post(self.LOGIN_FOR_TOKEN_URL, payload)

        self.assertNotIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_response_204_when_refresh_token_provided(self):
        payload = {"email": self.EMAIL, "password": self.PASSWORD}

        login_res = self.client.post(self.LOGIN_FOR_TOKEN_URL, payload)
        login_res_body = login_res.json()
        token_data = {"refresh": login_res_body["refresh"]}
        logout_res = self.client.post(
            self.LOGOUT_TO_BLACKLIST_REFRESH_TOKEN_URL, token_data
        )

        self.assertEqual(
            logout_res.status_code, status.HTTP_204_NO_CONTENT
        )

    def test_logout_response_400_when_no_refresh_token(self):
        token_data = {"refresh": ""}
        logout_res = self.client.post(
            self.LOGOUT_TO_BLACKLIST_REFRESH_TOKEN_URL, token_data
        )
        logout_res_body = logout_res.json()

        self.assertEqual(
            logout_res.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertIn(
            "This field may not be blank.", logout_res_body["refresh"]
        )

    def test_logout_response_400_when_bad_refresh_token(self):
        token_data = {"refresh": "wrong_token"}
        logout_res = self.client.post(
            self.LOGOUT_TO_BLACKLIST_REFRESH_TOKEN_URL, token_data
        )
        logout_res_body = logout_res.json()

        self.assertEqual(
            logout_res.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertIn("Token is invalid or expired", logout_res_body[0])

    def test_token_blacklisted_on_logout(self):
        payload = {"email": self.EMAIL, "password": self.PASSWORD}
        login_res = self.client.post(self.LOGIN_FOR_TOKEN_URL, payload)
        login_res_body = login_res.json()
        token_data = {"refresh": login_res_body["refresh"]}

        self.client.post(
            self.LOGOUT_TO_BLACKLIST_REFRESH_TOKEN_URL, token_data
        )
        second_logout_try_res = self.client.post(
            self.LOGOUT_TO_BLACKLIST_REFRESH_TOKEN_URL, token_data
        )
        logout_res_body = second_logout_try_res.json()

        self.assertEqual(
            second_logout_try_res.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("Token is invalid or expired", logout_res_body[0])
