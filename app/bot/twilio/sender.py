from django.conf import settings
from twilio.rest import Client as TwilioClient
from twilio.base.exceptions import TwilioRestException
from app.base import BaseSingletone
from app import email
from accounts.models import User


class SenderClient(BaseSingletone):
    def __init__(self):
        self.twilio_client = TwilioClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    def send(self, users, msg_body_formatter, from_scheme="whatsapp", to_scheme="whatsapp"):
        from_ = f"{from_scheme}:{settings.TWILIO_PHONE_NUMBER}"
        fails = []
        for user in users:
            to = f"{to_scheme}:{user.phone}"
            msg_body = msg_body_formatter(user)
            try:
                self.twilio_client.messages.create(body=msg_body, from_=from_, to=to)
            except TwilioRestException:
                fails.append(user)

        if fails:
            msg_subject_formatter = lambda _user: f"[Twilio] Failed to send SMS from {from_}"
            formatted_users = "\n\n".join(map(str, fails))
            msg_body_formatter = lambda user: (
                f"Hi {user.first_name},\n\n"
                "I wasn't able to send an SMS to the following user(s):\n\n"
                f"{formatted_users}"
            )
            email.SenderClient().send(User.objects.filter(is_staff=True), msg_subject_formatter, msg_body_formatter)
