from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from .managers import UserManager
from app.base import BaseModel



class User(BaseModel, AbstractUser):
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "password"]

    balance = models.PositiveIntegerField(default=0, verbose_name="account balance")

    objects = UserManager()

    @property
    def number_of_tickets(self):
        return self.balance // settings.TICKET_COST

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save(*args, **kwargs)

    def restore(self, *args, **kwargs):
        self.is_active = True
        self.save(*args, **kwargs)

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
