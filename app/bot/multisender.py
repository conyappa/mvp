from .telegram import sender as telegram_sender
from .twilio import sender as twilio_sender


def send(users, msg_body_formatter, telegram=False, telegram_kwargs={}, twilio=False, twilio_kwargs={}):
    if telegram:
        telegram_users = users.filter(telegram_id__isnull=False)
        telegram_sender.send(telegram_users, msg_body_formatter, **telegram_kwargs)

    if twilio:
        twilio_users = users.filter(phone__isnull=False)
        twilio_sender.send(twilio_users, msg_body_formatter, **twilio_kwargs)
