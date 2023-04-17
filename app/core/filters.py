from typing import List

import django_filters
from core.models import Book
from django_filters import CharFilter


class BookFilter(django_filters.FilterSet):
    """
    Filter class for book api.
    Enables filtering by author and title on the QuerySet.
    """

    author: CharFilter = django_filters.CharFilter(
        lookup_expr="icontains"
    )

    class Meta:
        model: Book = Book
        fields: List[str] = ["author", "title"]
