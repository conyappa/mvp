import logging
from django.utils import timezone
from django.conf import settings
from lottery.models import Draw
from accounts.models import User
from bot import sender
from .helpers import use_scheduler


logger = logging.getLogger(__name__)


multisender = sender.MultiSender


def remind_of_new_draw():
    # Broadcast a notification.
    multisender.send(
        users=User.objects.all(),
        msg_body_formatter=lambda _user: (
            f"Recordatorio: ¡Hoy a las {settings.FORMATTED_DRAW_RESULTS_TIME} comienza el sorteo! 🎉"
            f"\n\nA las {settings.FORMATTED_NEW_DRAW_CREATION_TIME} se generarán tus boletos;"
            " recuerda depositar tus ahorros antes de esa hora para aumentar tus probabilidades de ganar 🍀."
            "\n\nEnvía /saldo para consultar tu saldo y ver cuánto te falta para obtener tu próximo boleto."
        ),
        interfaces=("telegram",),
    )


@use_scheduler
def add_new_draw_reminder_cycle(scheduler):
    scheduler.add_job(
        remind_of_new_draw,
        "cron",
        day_of_week=settings.NEW_DRAW_WEEKDAY,
        hour=settings.NEW_DRAW_REMINDER_HOUR,
        minute=settings.DRAW_RESULTS_MINUTE,
    )


def create_new_draw():
    # Create a new draw.
    Draw.objects.create(users=User.objects.all(), start_date=timezone.localdate())
    # Broadcast a notification.
    multisender.send(
        users=User.objects.all(),
        msg_body_formatter=lambda _user: (
            f"Ya se han generado tus boletos para el sorteo de las {settings.FORMATTED_DRAW_RESULTS_TIME} 😱."
            "\n\n¡Envía /boletos para revisarlos!"
        ),
        interfaces=("telegram",),
    )


@use_scheduler
def add_new_draw_creation_cycle(scheduler):
    scheduler.add_job(
        create_new_draw,
        "cron",
        day_of_week=settings.NEW_DRAW_WEEKDAY,
        hour=settings.NEW_DRAW_CREATION_HOUR,
        minute=settings.DRAW_RESULTS_MINUTE,
    )


def publish_new_draw():
    # Choose the first result.
    draw = Draw.objects.current()
    draw.choose_result()

    # Send a notification.
    multisender.send(
        users=User.objects.all(),
        msg_body_formatter=lambda _user: (
            "¡Ha comenzado el sorteo! 🎉"
            f"El primer número es el *{draw.results[0]}* 🎰\n\n"
            "Envía /boletos para ver si le achuntaste."
        ),
        interfaces=("telegram",),
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
        interfaces=("telegram",),
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
            f"{draw.formatted}\n\n"
            f"¡Ganaste *${user.current_prize}*! 🤑"
        ),
        interfaces=("telegram",),
    )


def ongoing_draw_cycle():
    now = timezone.localtime()
    draw_exists = Draw.objects.exists()

    if now.weekday() == settings.NEW_DRAW_WEEKDAY:
        publish_new_draw()
    elif (now.weekday() == settings.END_DRAW_WEEKDAY) and draw_exists:
        end_current_draw()
    elif draw_exists:
        choose_number_from_current_draw()


@use_scheduler
def add_ongoing_draw_cycle(scheduler):
    scheduler.add_job(ongoing_draw_cycle, "cron", hour=settings.DRAW_RESULTS_HOUR, minute=settings.DRAW_RESULTS_MINUTE)
