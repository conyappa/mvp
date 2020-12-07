import logging
import random as rd
import datetime as dt
from django.db import models
from django.conf import settings
from django.utils import timezone
from app.base import BaseModel


logger = logging.getLogger(__name__)


def generate_random_picks():
    return rd.sample(population=settings.TICKET_PICK_RANGE, k=settings.TICKET_LENGTH)


def generate_result_pool():
    return list(settings.TICKET_PICK_RANGE)


class Draw(BaseModel):
    date = models.DateField(verbose_name="creation date")
    pool = models.JSONField(default=generate_result_pool, verbose_name="result pool")
    results = models.JSONField(blank=True, default=list, verbose_name="results")

    def choose_results(self, k):
        results = rd.sample(population=self.pool, k=k)
        self.pool = list(set(self.pool) - set(results))
        self.results += results
        self.save()

    def attach_results_schedule(self, scheduler):
        for days_delta in range(1, 8):
            run_date = self.date + dt.timedelta(days=days_delta, hours=settings.DRAW_RESULTS_HOUR)
            scheduler.add_job(self.choose_results, "date", run_date=run_date, kwargs={"k": 1})

    @classmethod
    def create(cls, scheduler):
        draw = cls.objects.create(date=timezone.now())
        logger.error(draw)
        draw.attach_results_schedule(scheduler)

    @classmethod
    def attach_creation_schedule(cls, scheduler):
        scheduler.add_job(
            cls.create,
            "cron",
            day_of_week=settings.NEW_DRAW_DAY_OF_WEEK,
            hour=settings.NEW_DRAW_HOUR,
            kwargs={"scheduler": scheduler},
        )

    def __str__(self):
        return f"{self.date}\n{self.pool}\n{self.results}"


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
