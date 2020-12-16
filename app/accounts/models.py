from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from app.base import BaseModel


class UserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def everything(self):
        return super().get_queryset()

    def create_superuser(self, **fields):
        fields.setdefault("is_staff", True)
        fields.setdefault("is_superuser", True)
        return self.create(**fields)


class User(BaseModel, AbstractUser):
    USERNAME_FIELD = "phone"

    username = None
    phone = PhoneNumberField(
        unique=True,
        error_messages={"unique": "A user with that phone number already exists."},
        verbose_name="phone number",
    )

    balance = models.PositiveIntegerField(default=0, verbose_name="balance")
    extra_tickets = JSONField(default=generate_initial_extra_tickets)

    objects = UserManager()

    def __init__(self, *args, **kwargs):
        ret = super().__init__(*args, **kwargs)
        if "password" in kwargs:
            self.set_password(kwargs["password"])
        return ret

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save(*args, **kwargs)

    def restore(self, *args, **kwargs):
        self.is_active = True
        self.save(*args, **kwargs)

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    @property
    def number_of_tickets(self):
        return min(settings.MAX_TICKETS, self.balance // settings.TICKET_COST)

    @property
    def current_tickets(self):
        return self.tickets.current()

    @property
    def current_prize(self):
        return sum(map(lambda x: x.prize, self.current_tickets))

    def __str__(self):
        return str(self.phone)
