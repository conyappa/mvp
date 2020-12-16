import datetime as dt
from django.utils import timezone
from django.conf import settings
from lottery.models import Draw
from accounts.models import User
from bot.sender import SenderClient
from .helpers import use_scheduler


# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


sender = SenderClient()


def draw_cycle():
    now = timezone.now()
    all_users = Users.objects.all()

    if now.weekday() == settings.NEW_DRAW_WEEKDAY:
        if Draw.objects.exists():
            # End the previous draw.
            previous_draw = Draw.objects.current()
            previous_draw.conclude()
            sender.send_sms(users=all_users, msg_body="¡Ha finalizado el sorteo! Los resultados fueron...")

        # Create a new draw.
        current_draw = Draw.objects.create(start_date=now.date())
        current_draw.create_tickets()
        current_draw.choose_result()
        sender.send_sms(users=all_users, msg_body=f"¡Ha comenzado un nuevo sorteo! El número de hoy es...")

    elif Draw.objects.exists():
        current_draw.choose_result()
        sender.send_sms(users=all_users, msg_body=f"El número de hoy es...")


@use_scheduler
def add_draw_cycle_job(scheduler):
    scheduler.add_job(draw_cycle, "cron", hour=settings.DRAW_RESULTS_HOUR, minute=settings.DRAW_RESULTS_MINUTE)
