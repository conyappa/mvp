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


def draw_cycle():
    now = timezone.localtime()
    all_users = User.objects.all()
    sender = SenderClient()

    if now.weekday() == settings.NEW_DRAW_WEEKDAY:
        if Draw.objects.exists():
            # End the previous draw.
            previous_draw = Draw.objects.current()
            previous_draw.conclude()
            # Broadcast a notification.
            sender.send_sms(users=all_users, msg_body=(
                "¡Ha finalizado el sorteo! Los resultados son:\n\n"
                f"{formatted_results}"
                f"\n\n¡Ganaste *${user.current_prize}*! 🤑"
            ))

        # Create a new draw.
        current_draw = Draw.objects.create(start_date=now.date())
        current_draw.create_tickets()
        current_draw.choose_result()
        # Broadcast a notification.
        sender.send_sms(users=all_users, msg_body=(
            "¡Ha comenzado el nuevo sorteo! "
            f"El primer número es {current_draw.results[0]}"
        ))

    elif Draw.objects.exists():
        # Continue with the ongoing draw.
        current_draw = Draw.objects.current()
        current_draw.choose_result()
        # Broadcast a notification.
        formatted_time = dt.time(hour=settings.DRAW_RESULTS_HOUR, minute=settings.DRAW_RESULTS_MINUTE).isoformat(
            timespec="minutes"
        )
        sender.send_sms(users=all_users, msg_body=(
            "¡Llegó la hora de sacar un número! "
            f"El número del hoy es el *{current_draw.results[-1]}* 🎉\n\n"
            "Envía 'results' para revisar los resultados de la semana."
        ))


@use_scheduler
def add_draw_cycle_job(scheduler):
    scheduler.add_job(draw_cycle, "cron", hour=settings.DRAW_RESULTS_HOUR, minute=settings.DRAW_RESULTS_MINUTE)
