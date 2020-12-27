import logging
from django.utils import timezone
from django.conf import settings
from lottery.models import Draw
from accounts.models import User
from bot import multisender
from .helpers import use_scheduler


logger = logging.getLogger(__name__)


def create_new_draw(timestamp):
    all_users = User.objects.all()
    # Create a new draw.
    draw = Draw.objects.create(users=all_users, start_date=timestamp.date())
    draw.choose_result()
    # Send a notification.
    multisender.send(
        users=all_users,
        msg_body_formatter=lambda _user: (
            "¡Ha comenzado un nuevo sorteo! "
            f"El primer número es el *{draw.results[0]}* 🎰\n\n"
            "Envía /boletos para ver si le achuntaste."
        ),
        telegram=True,
        twilio=False,
    )


def end_current_draw():
    # End the ongoing draw.
    draw = Draw.objects.current()
    draw.choose_result()
    draw.conclude()
    # Send a notification.
    multisender.send(
        users=User.objects.all(),
        msg_body_formatter=lambda user: (
            "¡Finalizó el sorteo! Los resultados fueron:\n\n"
            f"{draw.formatted_results}\n\n"
            f"¡Ganaste *${user.current_prize}*! 🤑"
        ),
        telegram=True,
        twilio=False,
    )


def choose_number_from_current_draw():
    # Continue with the ongoing draw.
    draw = Draw.objects.current()
    draw.choose_result()
    # Broadcast a notification.
    multisender.send(
        users=User.objects.all(),
        msg_body_formatter=lambda _user: (
            "¡Llegó la hora de sacar un número!\n"
            f"El número de hoy es el *{draw.results[-1]}* 🎉\n\n"
            "Envía /resultados para revisar los resultados de la semana."
        ),
        telegram=True,
        twilio=False,
    )


def draw_cycle():
    now = timezone.localtime()
    draw_exists = Draw.objects.exists()

    if now.weekday() == settings.NEW_DRAW_WEEKDAY:
        create_new_draw(now)
    elif (now.weekday() == settings.END_DRAW_WEEKDAY) and draw_exists:
        end_current_draw()
    elif draw_exists:
        choose_number_from_current_draw()


@use_scheduler
def add_draw_cycle_job(scheduler):
    scheduler.add_job(draw_cycle, "cron", hour=settings.DRAW_RESULTS_HOUR, minute=settings.DRAW_RESULTS_MINUTE)
