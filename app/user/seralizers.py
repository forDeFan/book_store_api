from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """User serializer for API views."""

    class Meta:
        """Model and additional args to be passed to serializer (extra_kwargs)."""

        model = get_user_model()
        fields = ["email", "password", "name"]
        # Prevent to return password in Response.
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5}
        }

    def create(self, validated_data):
        """Creates and return user."""
        return get_user_model().objects.create_user(**validated_data)
