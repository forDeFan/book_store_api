"""Book API views."""

from typing import List, Tuple

from book.serializers import BookSerializer
from core.filters import BookFilter
from core.models import Book
from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.response import Response


class BookViewSet(viewsets.ModelViewSet):
    """Class based Django views to manage book API."""

    serializer_class: BookSerializer = BookSerializer
    queryset: QuerySet[Book] = Book.objects.all()
    filter_backends: DjangoFilterBackend = [DjangoFilterBackend]
    filter_class: BookFilter = BookFilter

    def get_permissions(self) -> List:
        """
        Overwritten permission function
        to manually set particular permission type
        to user role.
        Actions defined in Django ViewSet maps to
        get, post etc. (http methods).

        I.e:
            Admin can add, delete, modify book.
            User can search for books without authentication
            nor being admin.

        """
        admin_actions: List[str] = [
            "create",  # post
            "destroy",  # del
            "update",  # patch
            "partial_update",
        ]
        user_actions: List[str] = ["retrieve", "list"]  # get

        if self.action in admin_actions:
            permission_classes: Tuple = (
                IsAdminUser,
                IsAuthenticated,
            )
        if self.action in user_actions:
            permission_classes: Tuple = (AllowAny,)
        
        else:
            permission_classes: Tuple = (
                IsAdminUser,
                IsAuthenticated,
            )

        return [permission() for permission in permission_classes]

    def get_queryset(self) -> QuerySet[Book]:
        """
        Return list (QuerySet) of filtered books.
        Books can be filtered by title or by author - separate and as joined query.

        If single param: no query param, param empty or wrong param name - list of all books will be returned.

        If joined params:
            If one of the params wrong or record not in db - empty list will be returned in response.
            If one of params empty - query will be performed for one param only (if no record empty list
            will be returned in response).

        All users can list books without logging in into service.
        """
        author: str = self.request.GET.get("author", None)
        title: str = self.request.GET.get("title", None)
        queryset: QuerySet[Book] = Book.objects.all()

        if author:
            queryset = queryset.filter(author__contains=author)
        if title:
            queryset = queryset.filter(title__contains=title)

        self.queryset = queryset
        return self.queryset

    def perform_create(self, serializer) -> None:
        """
        Create new book in the service.
        Only admin user can perform that action.
        """
        serializer.save()

    def perform_update(self, serializer) -> None:
        """
        Update/ partial update book in the service.
        Only admin user can perform that action.
        """
        before_update: Book = (
            self.get_object()
        )  # Values used if not provided in update request
        new_title: str = self.request.data.get(
            "title", before_update.title
        )
        new_author: str = self.request.data.get(
            "author", before_update.author
        )
        new_pub_date: str = self.request.data.get(
            "published_date", before_update.published_date
        )

        serializer.save(
            title=new_title,
            author=new_author,
            published_date=new_pub_date,
        )

    def destroy(self, request, *args, **kwargs) -> Response:
        """
        Delete book from the service.
        Only admin can perform that action.
        """
        return super().destroy(request, *args, **kwargs)
