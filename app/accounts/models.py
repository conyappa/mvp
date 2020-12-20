from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from app.base import BaseModel


def generate_initial_extra_tickets_ttl():
    return []


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
    USERNAME_FIELD = "email"

    username = None
    phone = PhoneNumberField(
        unique=True,
        blank=True,
        null=True,
        error_messages={"unique": "A user with that phone number already exists."},
        verbose_name="phone number",
    )
    telegram_id = models.PositiveBigIntegerField(
        unique=True,
        blank=True,
        null=True,
        error_messages={"unique": "A user with that Telegram ID already exists."},
        verbose_name="Telegram user ID",
    )

    balance = models.PositiveIntegerField(default=0, verbose_name="balance")
    winnings = models.PositiveIntegerField(default=0, verbose_name="winnings")
    extra_tickets_ttl = models.JSONField(
        blank=True, default=generate_initial_extra_tickets_ttl, verbose_name="extra tickets TTL"
    )

    objects = UserManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "password" in kwargs:
            self.set_password(kwargs["password"])

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save(*args, **kwargs)

    def restore(self, *args, **kwargs):
        self.is_active = True
        self.save(*args, **kwargs)

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def award_prize(self, value):
        self.balance += value
        self.winnings += value
        self.save()

    @property
    def extra_tickets(self):
        self.extra_tickets_ttl = list(filter(bool, self.extra_tickets_ttl))
        self.save()
        return len(self.extra_tickets_ttl)

    @property
    def number_of_tickets(self):
        return min(settings.MAX_TICKETS, (self.balance // settings.TICKET_COST) + self.extra_tickets)

    @property
    def current_tickets(self):
        return self.tickets.current()

    @property
    def current_prize(self):
        return sum(map(lambda x: x.prize, self.current_tickets))

    def __str__(self):
        return str(self.phone)
