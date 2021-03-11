from logging import getLogger
from django.utils import timezone
from django.conf import settings
from lottery.models import Draw
from accounts.models import User
from bot.telegram.sender import Client as TelegramClient
from banking.fintoc import Interface as FintocInterface
from .helpers import use_scheduler


logger = getLogger(__name__)


#####################
# NEW DRAW REMINDER #
#####################


def remind_of_new_draw():
    # Broadcast a notification.
    TelegramClient().send_async(
        users=User.objects.all(),
        msg_formatter=lambda _user: (
            f"Recordatorio: ¡Hoy a las {settings.FORMATTED_DRAW_RESULTS_TIME} comienza el sorteo! 🎉"
            f"\n\nA las {settings.FORMATTED_NEW_DRAW_CREATION_TIME} se generarán tus boletos;"
            " recuerda depositar tus ahorros antes de esa hora para aumentar tus probabilidades de ganar 🍀."
            "\n\nEnvía /saldo para consultar tu saldo y ver cuánto te falta para obtener tu próximo boleto."
        ),
    )


@use_scheduler
def add_new_draw_reminder_cycle(scheduler):
    scheduler.add_job(
        remind_of_new_draw,
        trigger="cron",
        day_of_week=settings.NEW_DRAW_WEEKDAY,
        hour=settings.NEW_DRAW_REMINDER_HOUR,
        minute=settings.DRAW_RESULTS_MINUTE,
    )


#####################
# NEW DRAW CREATION #
#####################


def create_new_draw():
    # Create a new draw.
    Draw.objects.create(users=User.objects.all(), start_date=timezone.localdate())
    # Broadcast a notification.
    TelegramClient().send_async(
        users=User.objects.all(),
        msg_formatter=lambda _user: (
            f"Ya se han generado tus boletos para el sorteo de las {settings.FORMATTED_DRAW_RESULTS_TIME} 😱."
            "\n\n¡Envía /boletos para revisarlos!"
        ),
    )


@use_scheduler
def add_new_draw_creation_cycle(scheduler):
    scheduler.add_job(
        create_new_draw,
        trigger="cron",
        day_of_week=settings.NEW_DRAW_WEEKDAY,
        hour=settings.NEW_DRAW_CREATION_HOUR,
        minute=settings.DRAW_RESULTS_MINUTE,
    )


######################
# ONGOING DRAW CYCLE #
######################


def publish_new_draw():
    # Choose the first result.
    draw = Draw.objects.current()
    draw.choose_result()

    # Send a notification.
    TelegramClient().send_async(
        users=User.objects.all(),
        msg_formatter=lambda _user: (
            "¡Ha comenzado el sorteo! 🎉"
            f"El primer número es el *{draw.results[0]}* 🎰."
            "\n\nEnvía /boletos para ver si le achuntaste."
        ),
    )


def choose_number_from_current_draw():
    # Continue with the ongoing draw.
    draw = Draw.objects.current()
    draw.choose_result()
    # Broadcast a notification.
    TelegramClient().send_async(
        users=User.objects.all(),
        msg_formatter=lambda _user: (
            "¡Llegó la hora de sacar un número!"
            f"\nEl número de hoy es el *{draw.results[-1]}* 🎉."
            "\n\nEnvía /boletos para revisar cuánto has ganado."
            "\n\nEnvía /resultados para ver los números de la semana."
        ),
    )


def end_current_draw():
    # End the ongoing draw.
    draw = Draw.objects.current()
    draw.choose_result()
    draw.conclude()
    # Send a notification.
    TelegramClient().send_async(
        users=User.objects.all(),
        msg_formatter=lambda user: (
            "¡Finalizó el sorteo! Los resultados fueron:"
            f"\n\n{draw.formatted}"
            f"\n\n¡Ganaste *${user.current_prize}*! 🤑"
        ),
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
    scheduler.add_job(
        ongoing_draw_cycle, trigger="cron", hour=settings.DRAW_RESULTS_HOUR, minute=settings.DRAW_RESULTS_MINUTE
    )


##################
# BANK MOVEMENTS #
##################


@use_scheduler
def add_fintoc_movements_fetcher(scheduler):
    fintoc_interface = FintocInterface()
    scheduler.add_job(
        fintoc_interface.fetch_movements, trigger="cron", minutes=settings.FINTOC_MOVEMENTS_FETCH_MINUTES_INTERVAL
    )
