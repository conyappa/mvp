from twilio.rest import Client
from django.conf import settings


class SenderClient:
    def __init__(self):
        self.twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    def send(users, msg_body, from_scheme="whatsapp", to_scheme="whatsapp"):
        from_ f"{from_scheme}:{settings.TWILIO_PHONE_NUMBER}"
        for user in users:
            to = f"{to_scheme}:{user.phone}"
            self.twilio_client.messages.create(body=msg_body, from_=from_, to=to)
