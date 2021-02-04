from telegram.constants import PARSEMODE_MARKDOWN
from telegram import Bot
from django.conf import settings
from app import email
from accounts.models import User


def send(users, msg_body_formatter, parse_mode=PARSEMODE_MARKDOWN):
    client = Bot(token=settings.TELEGRAM_TOKEN)
    fails = set()

    for user in users:
        msg_body = msg_body_formatter(user)
        try:
            client.send_message(chat_id=user.telegram_id, text=msg_body, parse_mode=parse_mode)
        except Exception as e:
            fails.add((user, e))

    if fails:
        msg_subject_formatter = lambda _user: "Failed to send Telegram SMS"
        formatted_users = "\n\n".join(map(lambda u, e: f"{u}: {e}", fails))
        msg_body_formatter = lambda user: (
            f"Hi {user.first_name},\n\n"
            "I wasn't able to send a Telegram SMS to the following user(s):\n\n"
            f"{formatted_users}"
        )
        email.send(User.objects.filter(is_staff=True), msg_subject_formatter, msg_body_formatter)
