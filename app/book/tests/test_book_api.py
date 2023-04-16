from core.models import Book, User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

BOOKS_URL = reverse("book:book-list")


def create_book(**params) -> Book:
    """
    Create and return books for tests with defaults values.
    Defaults can be overtitten on instantiation.
    """
    default_values = {
        "title": "test_title_1",
        "author": "test_author_1",
        "published_date": "2023-01-01",
    }
    default_values.update(params)
    book = Book.objects.create(**default_values)

    return book


def detail_url(book_id):
    """Returns url with book id in it."""
    return reverse("book:book-detail", args=[book_id])


class PublicBookTests(TestCase):
    """API calls to endpoints where authentication/ authorization not needed."""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_book_listing_200_for_not_logged_user(
        self,
    ):
        """Test listing of all books without logging in."""

        create_book()
        create_book(title="test_title_2")
        res = self.client.get(BOOKS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(Book.objects.all()))

    def test_book_filtering_200_for_not_logged_user(
        self,
    ):
        """Test filtering without logging in."""

        create_book()
        create_book(title="test_title_2")
        res = self.client.get(
            BOOKS_URL, QUERY_STRING="title=test_title_1"
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("test_title_1", res.data[0]["title"])

    def test_book_update_401_if_not_logged_in(self):
        book = create_book()
        update_payload = {
            "title": "changed_test_title_1",
        }

        url = detail_url(book.id)
        res = self.client.patch(url, update_payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            0, len(Book.objects.filter(title="changed_test_title_1"))
        )

    def test_book_delete_401_if_not_logged_in(self):
        """Test that not logged in user can't delete books."""
        book = create_book()

        url = detail_url(book.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(1, len(Book.objects.all()))


class PrivateBookAdminUserTests(TestCase):
    """
    API calls made by authenticated admin user.
    """

    def setUp(self) -> None:
        self.client = APIClient()
        admin = User.objects.create_superuser(
            email="admin@test.com", password="test_pass"
        )
        self.client.force_authenticate(admin)

    def test_book_creation_201_when_admin(self):
        """Test if book created when admin user."""
        payload = {
            "title": "test_title_1",
            "author": "test_author_1",
            "published_date": "2023-01-01",
        }
        res = self.client.post(BOOKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, len(Book.objects.all()))

    def test_book_update_200_when_admin(self):
        book = create_book()
        update_payload = {
            "title": "changed_test_title_1",
        }

        url = detail_url(book.id)
        res = self.client.patch(url, update_payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("changed_test_title_1", res.data["title"])

    def test_book_delete_204_if_admin(self):
        """Test that admin can delete books."""
        book = create_book()

        url = detail_url(book.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(0, len(Book.objects.all()))


class PrivateBookNotAdminUserTests(TestCase):
    """
    API calls made by authenticated non-admin user.
    """

    def setUp(self) -> None:
        self.client = APIClient()
        user = User.objects.create_user(
            email="user@test.com", password="test_pass"
        )
        self.client.force_authenticate(user)

    def test_book_creation_403_when_not_admin(self):
        """Test if book not created when not admin user."""

        payload = {
            "title": "test_title_1",
            "author": "test_author_1",
            "published_date": "2023-01-01",
        }
        res = self.client.post(BOOKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(0, len(Book.objects.all()))

    def test_book_update_403_when_not_admin(self):
        book = create_book()
        update_payload = {
            "title": "changed_test_title_1",
        }

        url = detail_url(book.id)
        res = self.client.patch(url, update_payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn("changed_test_title_1", Book.objects.all())

    def test_book_delete_403_when_not_admin(self):
        """Test that not logged in user can't delete books."""
        book = create_book()

        url = detail_url(book.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(1, len(Book.objects.all()))