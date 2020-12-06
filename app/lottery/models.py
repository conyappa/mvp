import random as rd
from django.db import models
from app.base import BaseModel


MAX_PICK_NUMBER = 20


class Ticket(BaseModel):
    week = models.DateField(auto_now=False, auto_now_add=False, verbose_name="week")
    picks = models.JSONField(default=Ticket.generate_random_picks)

    @staticmethod
    def generate_random_picks():
        return rd.sample(range(1, MAX_PICK_NUMBER), 7)
