from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    avatar = models.ImageField(
        upload_to="avatars/",
        default="static/images/avatar.svg",
        blank=True,
        null=True,
    )