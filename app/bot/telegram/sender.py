from logging import getLogger
import threading as th
from telegram import Bot
from telegram.constants import PARSEMODE_MARKDOWN
from django.conf import settings
from app import email
from app.utils import Singleton, Delayer, PseudoUser
from accounts.models import User


logger = getLogger(__name__)


class Client(metaclass=Singleton):
    def __init__(self):
        self.bot = Bot(token=settings.TELEGRAM_TOKEN)
        self.delayer = Delayer(
            max_bulk_size=settings.TELEGRAM_MAX_BULK_SIZE, delay_seconds=settings.TELEGRAM_DELAY_SECONDS
        )

    def send(self, msg_formatter, users=[], chat_ids=[], report_errors=True, get_kwargs=lambda _user: {}):
        fails = set()

        pseudo_users = [PseudoUser(telegram_id=chat_id) for chat_id in chat_ids]

        for user in users + pseudo_users:
            try:
                kwargs = {"parse_mode": PARSEMODE_MARKDOWN, **get_kwargs(user)}
                msg_body = msg_formatter(user)

                with self.delayer:
                    self.bot.send_message(chat_id=user.telegram_id, text=msg_body, **kwargs)

            except Exception as e:
                logger.error(f"Unable to send a Telegram message: {e}")
                fails.add((user, e))

        if report_errors and fails:
            self.report_fails(fails)

    def send_async(self, *args, **kwargs):
        th.Thread(target=self.send, args=args, kwargs=kwargs).start()

    def report_fails(self, fails):
        msg_subject_formatter = lambda _user: "Failed to send message(s)"

        formatted_users = "\n\n".join(map(lambda fail: f"{fail[0]}: {fail[1]}", fails))
        msg_formatter = lambda user: (
            f"Hi {user.first_name},\n\n"
            "I wasn't able to send a Telegram message to the following user(s):\n\n"
            f"{formatted_users}"
        )

        staff_users = User.objects.filter(is_staff=True)
        email.send(staff_users, msg_subject_formatter, msg_formatter)
