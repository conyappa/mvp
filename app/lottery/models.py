import itertools
import copy as cp
from random import SystemRandom
from django.db import models
from django.conf import settings
from django.db import transaction
from app.base import BaseModel
from app.utils import q


rd = SystemRandom()  # Alternative random generator that uses os.urandom.


def generate_random_picks():
    return rd.sample(population=Draw.objects.current().pool, k=7)


def generate_result_pool():
    return list(settings.PICK_RANGE)


class DrawManager(models.Manager):
    def current(self):
        # This method assumes there always is an ongoing draw.
        return self.latest("created_at")

    def create(self, users, **fields):
        draw = super().create(**fields)
        all_tickets = []
        with transaction.atomic():
            for user in users:
                user_tickets = draw.generate_user_tickets(user=user)
                all_tickets += user_tickets
                user.consume_extra_tickets()
            Ticket.objects.bulk_create(objs=all_tickets)
        return draw


class Draw(BaseModel):
    class Meta:
        ordering = ["-created_at"]

    start_date = models.DateField(verbose_name="start date")
    pool = models.JSONField(default=generate_result_pool, verbose_name="result pool")
    results = models.JSONField(blank=True, default=list, verbose_name="results")

    objects = DrawManager()

    @property
    def filled_results(self):
        results = cp.deepcopy(self.results)
        results += itertools.repeat("?", 7 - len(results))
        return results

    @property
    def formatted(self):
        return "\n".join(map(lambda weekday, result: f"{weekday}: {result}", settings.WEEKDAYS, self.filled_results))

    def generate_user_tickets(self, user):
        return [Ticket(draw=self, user=user) for _ in range(user.number_of_tickets)]

    def include_new_user(self, user):
        with transaction.atomic():
            user_tickets = self.generate_user_tickets(user=user)
            Ticket.objects.bulk_create(objs=user_tickets)

    def choose_result(self):
        results = rd.sample(population=self.pool, k=1)
        self.pool = list(set(self.pool) - set(results))
        self.results += results
        self.save()

    def conclude(self):
        result_set = set(self.results)
        with transaction.atomic():
            for ticket in self.tickets.all():
                number_of_matches = len(result_set & set(ticket.picks))
                user = ticket.user
                value = settings.PRIZES[number_of_matches]
                user.award_prize(value)

    def __str__(self):
        return str(self.start_date)


class TicketManager(models.Manager):
    def current(self):
        return self.filter(draw=Draw.objects.current())


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

    objects = TicketManager()

    @property
    def number_of_matches(self):
        result_set = set(self.draw.results)
        return len(result_set & set(self.picks))

    @property
    def prize(self):
        return settings.PRIZES[self.number_of_matches]

    @property
    def formatted(self):
        draw_results = self.draw.results
        sorted_picks = sorted(self.picks)
        formatted_picks = ", ".join(
            map(lambda pick: f"*{pick}*" if (pick in draw_results) else str(pick), sorted_picks)
        )
        formatted_prize = f"_({q(self.number_of_matches, 'acierto')}: ${self.prize})_"
        return f"{formatted_picks}\n{' ' * 15}{formatted_prize}"

    def __str__(self):
        return f"{', '.join(map(str, self.picks))} @ {self.draw.start_date} of {self.user}"
