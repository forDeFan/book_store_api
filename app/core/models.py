# Used for typing
from __future__ import annotations

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    """Manager for custom system Users."""

    def create_user(
        self, email: str, password: str = None, **extra_fields
    ) -> User:
        """Custom create, save and return system user."""
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str) -> User:
        """Custom create, save and return system supersuer/ admin."""
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom system User class."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()

    # As user identifier
    USERNAME_FIELD = "email"


class Book(models.Model):
    """Book model class."""

    created = models.DateTimeField(auto_now=True)
    title = models.CharField(
        max_length=255, null=False, blank=False, unique=True
    )
    author = models.CharField(max_length=255, null=False, blank=False)
    published_date = models.DateField(blank=False)
    images = models.FileField(blank=True, upload_to="images/")

    def __str__(self) -> str:
        return self.title
