"""DB objects for User model."""

from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.accounts.managers import UserManager


class User(AbstractUser):
    """Custom User model."""

    username = None
    email = models.EmailField(blank=False, unique=True, verbose_name="Email")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """Model representation."""
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
