from twilio.rest import Client
from django.conf import settings


class SenderClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    def send_sms(self, users, msg_body, from_scheme="whatsapp", to_scheme="whatsapp"):
        from_ = f"{from_scheme}:{settings.TWILIO_PHONE_NUMBER}"
        for user in users:
            to = f"{to_scheme}:{user.phone}"
            self.twilio_client.messages.create(body=msg_body, from_=from_, to=to)
