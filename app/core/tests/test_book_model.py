from core.models import Book
from django.test import TestCase


class ModelTests(TestCase):
    """Tests for book model."""

    def test_create_book(self):
        """Test creating book successful."""

        title = "test_title"
        author = "test_author"
        published_date = "2023-01-01"
        images = None

        book = Book.objects.create(
            title=title,
            author=author,
            published_date=published_date,
            images=images,
        )

        self.assertEqual(book, Book.objects.filter(title=title).first())
