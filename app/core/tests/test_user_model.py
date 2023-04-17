from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTests(TestCase):
    """Tests for user model."""

    def test_create_user_with_email_successful(self):
        """Test creating user with email successful."""
        email = "test@test.com"
        password = "testPass"
        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email)
