import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager
from app.base import BaseModelMixin


class CustomUser(BaseModelMixin, AbstractUser):
    groups = None
    user_permissions = None

    objects = UserManager()
