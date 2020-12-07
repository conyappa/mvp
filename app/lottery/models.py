import random as rd
from django.db import models
from django.conf import settings
from app.base import BaseModel


def generate_random_picks():
    return rd.sample(population=settings.TICKET_PICK_RANGE, k=settings.TICKET_LENGTH)


def generate_result_pool():
    return list(settings.TICKET_PICK_RANGE)


class Draw(BaseModel):
    week = models.DateField(verbose_name="week")
    pool = models.JSONField(default=generate_result_pool)
    results = models.JSONField(default=list)

    def choose_results(self, k):
        results = rd.sample(population=self.pool, k=k)
        self.pool = list(set(self.pool) - set(results))
        self.results += results
        self.save()


class Ticket(BaseModel):
    picks = models.JSONField(default=generate_random_picks)
    draw = models.ForeignKey(
        "lottery.Draw",
        verbose_name="draw",
        related_name="tickets",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        "accounts.User",
        verbose_name="user",
        related_name="tickets",
        on_delete=models.CASCADE,
    )
