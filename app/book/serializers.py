"""Book API related serializers."""

from typing import List

from core.models import Book
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    """Book serializer."""

    class Meta:
        model = Book
        fields: str = "__all__"
        read_only_fields: List[str] = ["id"]
