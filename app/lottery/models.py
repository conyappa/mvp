import random as rd
from django.db import models
from django.conf import settings
from app.base import BaseModel


def generate_random_picks():
    return rd.sample(settings.PICK_RANGE, 7)


class Ticket(BaseModel):
    week = models.DateField(auto_now=False, auto_now_add=False, verbose_name="week")
    picks = models.JSONField(default=generate_random_picks)
    user = models.ForeignKey("accounts.User", verbose_name="user", related_name="tickets", on_delete=models.CASCADE)
