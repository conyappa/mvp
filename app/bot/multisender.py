from .telegram import sender as telegram_sender
from .twilio import sender as twilio_sender
from app.base import BaseSingletone


class MultiSenderClient(BaseSingletone):
    def __init__(self):
        self.telegram_client = telegram_sender.SenderClient()
        self.twilio_client = twilio_sender.SenderClient()

    def send(self, users, msg_body_formatter, telegram=False, telegram_kwargs={}, twilio=False, twilio_kwargs={}):
        telegram_users = users.filter(telegram_id__isnull=False)
        twilio_users = users.filter(phone__isnull=False)

        if telegram:
            telegram_users = users.filter(telegram_id__isnull=False)
            self.telegram_client.send(telegram_users, msg_body_formatter, **telegram_kwargs)

        if twilio:
            twilio_users = users.filter(phone__isnull=False)
            self.twilio_client.send(twilio_users, msg_body_formatter, **twilio_kwargs)
