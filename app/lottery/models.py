import random as rd
import datetime as dt
from django.db import models
from django.conf import settings
from django.db import transaction
from app.base import BaseModel
from accounts.models import User


def generate_random_picks():
    return rd.sample(population=settings.TICKET_PICK_RANGE, k=settings.TICKET_LENGTH)


def generate_result_pool():
    return list(settings.TICKET_PICK_RANGE)


class Draw(BaseModel):
    start_date = models.DateField(verbose_name="start date")
    pool = models.JSONField(default=generate_result_pool, verbose_name="result pool")
    results = models.JSONField(blank=True, default=list, verbose_name="results")


    def create_tickets(self):
        tickets = []
        for user in User.objects.all():
            user_tickets = [Ticket(draw=self, user=user) for _ in user.number_of_tickets]
            tickets += user_tickets
        with transaction.atomic():
            Ticket.objects.bulk_create(objs=tickets)

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
