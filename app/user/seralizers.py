from typing import Dict, List, OrderedDict

from core.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)
from rest_framework_simplejwt.tokens import (
    RefreshToken,
    Token,
    TokenError,
)


class UserSerializer(serializers.ModelSerializer):
    """User serializer for API views."""

    class Meta:
        """Model and additional args to be passed to serializer (extra_kwargs)."""

        model: User = get_user_model()
        fields: List[str] = ["email", "password", "name"]
        # Prevent to return password in Response.
        extra_kwargs: Dict[str, str] = {
            "password": {"write_only": True, "min_length": 5}
        }

    def create(self, validated_data: OrderedDict[str, str]) -> User:
        """Creates and return user."""
        return get_user_model().objects.create_user(**validated_data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    JWT token serializer.
    Returns encoded access and refresh token.
    """

    @classmethod
    def get_token(cls, user: User) -> Token:
        """
        Add custom fields and return encoded token.

        Args:
            user (User): for which token will be returned - if exists
        Returns:
            str: encoded token with custom fields
        """
        token: Token = super(
            MyTokenObtainPairSerializer, cls
        ).get_token(user)

        return token


class RefreshTokenSerializer(serializers.Serializer):
    """
    JWT refresh token serializer.
    Used to blacklist refresh token.
    """

    refresh = serializers.CharField()
    print(type(refresh))

    default_error_messages: Dict[str, str] = {
        "bad_token": ("Token is invalid or expired")
    }

    def validate(self, attrs: OrderedDict[str, str]) -> str:
        """Get refresh token from request."""
        self.token: str = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        """Blacklist refresh token."""
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad_token")
