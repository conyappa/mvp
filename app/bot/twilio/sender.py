from django.conf import settings
from twilio.rest import Client as TwilioClient
from app import email
from accounts.models import User


def send(users, msg_body_formatter, from_scheme="whatsapp", to_scheme="whatsapp"):
    client = TwilioClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    from_ = f"{from_scheme}:{settings.TWILIO_PHONE_NUMBER}"
    fails = set()

    for user in users:
        to = f"{to_scheme}:{user.phone}"
        msg_body = msg_body_formatter(user)
        try:
            client.messages.create(body=msg_body, from_=from_, to=to)
        except Exception:
            fails.add((user, e))

    if fails:
        msg_subject_formatter = lambda _user: f"Failed to send Twilio SMS from {from_}"
        formatted_users = "\n\n".join(map(lambda u, e: f"{u}: {e}", fails))
        msg_body_formatter = lambda user: (
            f"Hi {user.first_name},\n\n"
            "I wasn't able to send a Twilio SMS to the following user(s):\n\n"
            f"{formatted_users}"
        )
        email.send(User.objects.filter(is_staff=True), msg_subject_formatter, msg_body_formatter)
