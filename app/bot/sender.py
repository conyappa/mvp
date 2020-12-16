from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings
from django.core.mail import send_mass_mail
from accounts.models import User


class SenderClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    def send_email(self, users, msg_subject_formatter, msg_body_formatter, from_alias="mvp-bot"):
        from_domain = settings.EMAIL_HOST_USER.split("@")[1]
        from_ = f"{from_alias}@{from_domain}"
        datatuples = [(msg_subject_formatter(user), msg_body_formatter(user), from_, [user.email]) for user in users]
        send_mass_mail(datatuples)

    def send_sms(self, users, msg_body_formatter, from_scheme="whatsapp", to_scheme="whatsapp"):
        from_ = f"{from_scheme}:{settings.TWILIO_PHONE_NUMBER}"
        fails = []
        for user in users:
            to = f"{to_scheme}:{user.phone}"
            msg_body = msg_body_formatter(user)
            try:
                self.twilio_client.messages.create(body=msg_body, from_=from_, to="to")
            except TwilioRestException:
                fails.append(user)

        if fails:
            msg_subject_formatter = lambda _user: f"Failed to send SMS from {from_}"
            formatted_users = "\n\n".join(map(str, fails))
            msg_body_formatter = lambda user: (
                f"Hi {user.first_name},\n\n"
                "I wasn't able to send an SMS to the following user(s):\n\n"
                f"{formatted_users}"
            )
            self.send_email(User.objects.filter(is_staff=True), msg_subject_formatter, msg_body_formatter)
