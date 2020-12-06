import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager
from app.base import BaseModelMixin


class User(BaseModelMixin, AbstractUser):
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["username", "email", "password"]

    groups = None
    user_permissions = None

    objects = UserManager()
