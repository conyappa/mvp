from django.conf import settings
from django.core.mail import send_mass_mail
from .base import BaseSingletone


class SenderClient(BaseSingletone):
    @staticmethod
    def send(users, msg_subject_formatter, msg_body_formatter, from_alias="mvp-bot"):
        from_domain = settings.EMAIL_HOST_USER.split("@")[1]
        from_ = f"{from_alias}@{from_domain}"
        datatuples = [(msg_subject_formatter(user), msg_body_formatter(user), from_, [user.email]) for user in users]
        return send_mass_mail(datatuples)
