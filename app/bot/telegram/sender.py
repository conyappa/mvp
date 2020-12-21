from telegram import Bot
from django.conf import settings
from app.base import BaseSingletone
from app import email
from accounts.models import User


class SenderClient(BaseSingletone):
    def __init__(self):
        self.telegram_client = Bot(token=settings.TELEGRAM_TOKEN)

    def send(self, users, msg_body_formatter):
        # url = f"https://api.telegram.org/bot/{settings.TELEGRAM_TOKEN}/sendMessage"
        fails = set()

        for user in users:
            msg_body = msg_body_formatter(user)
            # requests.get(url=url, params={"chat_id": user.telegram_id, "text": msg_body})
            self.telegram_client.send_message(chat_id=user.telegram_id, text=msg_body)

        if fails:
            msg_subject_formatter = lambda _user: "[Telegram] Failed to send SMS"
            formatted_users = "\n\n".join(map(str, fails))
            msg_body_formatter = lambda user: (
                f"Hi {user.first_name},\n\n"
                "I wasn't able to send a Telegram SMS to the following user(s):\n\n"
                f"{formatted_users}"
            )
            email.SenderClient().send(User.objects.filter(is_staff=True), msg_subject_formatter, msg_body_formatter)
