import random as rd
import datetime as dt
from django.db import models
from django.conf import settings
from django.utils import timezone
from app.base import BaseModel
from scheduler.tasks import add_result_choice_job


def generate_random_picks():
    return rd.sample(population=settings.TICKET_PICK_RANGE, k=settings.TICKET_LENGTH)


def generate_result_pool():
    return list(settings.TICKET_PICK_RANGE)


class DrawManager(models.Manager):
    def create(*args, **kwargs):
        start_date = timezone.now() + dt.timedelta(days=settings.DRAW_CREATION_DAYS_DELTA)
        draw = super().create(start_date=start_date, *args, **kwargs)
        add_result_choice_job(draw=draw)
        return draw


class Draw(BaseModel):
    start_date = models.DateField(verbose_name="start date")
    pool = models.JSONField(default=generate_result_pool, verbose_name="result pool")
    results = models.JSONField(blank=True, default=list, verbose_name="results")

    objects = DrawManager()

    def choose_results(self, k):
        results = rd.sample(population=self.pool, k=k)
        self.pool = list(set(self.pool) - set(results))
        self.results += results
        self.save()

    def __str__(self):
        return f"{self.start_date}\n{self.pool}\n{self.results}"


class Ticket(BaseModel):
    picks = models.JSONField(default=generate_random_picks)
    draw = models.ForeignKey(
        to="lottery.Draw",
        verbose_name="draw",
        related_name="tickets",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        to="accounts.User",
        verbose_name="user",
        related_name="tickets",
        on_delete=models.CASCADE,
    )
