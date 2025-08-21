from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    
    Attributes:
        email (str): User's email address (unique).
    """
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        """Return human-readable representation of the user."""
        return self.username
