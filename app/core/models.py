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


class User(AbstractBaseUser, PermissionsMixin):
    """Custom system User class."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    objects = UserManager()

    # As user identifier
    USERNAME_FIELD = "email"
