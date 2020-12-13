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
        super().get_queryset()

    def create(self, **fields):
        user = super().create(**fields)
        user.set_password(fields["password"])
        user.save()

    def create_superuser(self, **fields):
        fields.setdefault("is_staff", True)
        fields.setdefault("is_superuser", True)
        return self.create(**fields)


class User(BaseModel, AbstractUser):
    USERNAME_FIELD = "phone"

    username = None

    twilio_account_sid = models.CharField(
        null=True,
        unique=True,
        error_messages={"unique": "A user with that Twilio account SID already exists."},
        max_length=100,
        verbose_name="Twilio account SID",
    )
    balance = models.PositiveIntegerField(default=0, verbose_name="balance")
    phone = PhoneNumberField(
        unique=True,
        error_messages={"unique": "A user with that phone number already exists."},
        verbose_name="phone number",
    )

    objects = UserManager()

    @property
    def number_of_tickets(self):
        return min(settings.MAX_TICKETS, self.balance // settings.TICKET_COST)

    @property
    def current_tickets(self):
        return self.tickets.current()

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save(*args, **kwargs)

    def restore(self, *args, **kwargs):
        self.is_active = True
        self.save(*args, **kwargs)

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.phone)
