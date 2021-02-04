import logging
import time
import threading as th
from telegram import Bot as TelegramClient
from telegram.constants import PARSEMODE_MARKDOWN
from twilio.rest import Client as TwilioClient
from django.conf import settings
from app import email
from accounts.models import User


logger = logging.getLogger(__name__)


class SenderInterfaceDelayer:
    def __init__(self, max_bulk_size, delay_seconds):
        self.lock = th.Lock()
        self.bulk_size = 0
        self.max_bulk_size = max_bulk_size
        self.delay_seconds = delay_seconds

    def __enter__(self):
        pass

    def __exit__(self, _type, _value, _traceback):
        with self.lock:
            self.bulk_size += 1

            if self.bulk_size >= self.max_bulk_size:
                time.sleep(self.delay_seconds)
                self.bulk_size = 0


class MultiSender:
    interfaces = {
        "telegram": {
            "client": TelegramClient(token=settings.TELEGRAM_TOKEN).send_message,
            "msg_body_name": "text",
            "get_defaults": lambda user: {"chat_id": user.telegram_id, "parse_mode": PARSEMODE_MARKDOWN},
            "delayer": SenderInterfaceDelayer(
                max_bulk_size=settings.TELEGRAM_MAX_BULK_SIZE, delay_seconds=settings.TELEGRAM_DELAY_SECONDS
            ),
        },
        "twilio": {
            "client": TwilioClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN).messages.create,
            "msg_body_name": "body",
            "get_defaults": lambda user: {
                "from_": f"whatsapp:{settings.TWILIO_PHONE_NUMBER}",
                "to": f"whatsapp:{user.phone}",
            },
            "delayer": SenderInterfaceDelayer(
                max_bulk_size=settings.TWILIO_MAX_BULK_SIZE, delay_seconds=settings.TWILIO_DELAY_SECONDS
            ),
        },
    }

    @staticmethod
    def wait_for(interface_name):
        counter = MultiSender.sent_counter[interface_name]

        with counter["lock"]:
            counter["value"] += 1
            interface_settings = MultiSender.interfaces[interface_name]["settings"]

            if counter["value"] > interface_settings["bulk_size"]:
                time.sleep(interface_settings["delay_secs"])
                counter["value"] = 0

    @staticmethod
    def send(users, msg_body_formatter, interfaces="all", interfaces_kwargs={}, report_errors=True):
        if interfaces == "all":
            interfaces = MultiSender.interfaces
        else:
            interfaces = {
                name: interface for (name, interface) in MultiSender.interfaces.items() if (name in interfaces)
            }

        for (interface_name, interface) in interfaces.items():
            fails = set()

            for user in users:
                try:
                    kwargs = {**interface["get_defaults"](user), **interfaces_kwargs.get(interface_name, {})}
                    kwargs[interface["msg_body_name"]] = msg_body_formatter(user)

                    with interface["delayer"]:
                        interface["client"](**kwargs)

                except Exception as e:
                    fails.add((user, e))

            if report_errors and fails:
                MultiSender.report_fails(interface_name, fails)

    @staticmethod
    def report_fails(interface_name, fails):
        msg_subject_formatter = lambda _user: f"Failed to send SMS from {interface_name} interface"

        formatted_users = "\n\n".join(map(lambda fail: f"{fail[0]}: {fail[1]}", fails))
        msg_body_formatter = lambda user: (
            f"Hi {user.first_name},\n\n"
            "I wasn't able to send a Twilio SMS to the following user(s):\n\n"
            f"{formatted_users}"
        )

        email.send(User.objects.filter(is_staff=True), msg_subject_formatter, msg_body_formatter)

    @staticmethod
    def send_async(*args, **kwargs):
        th.Thread(target=MultiSender.send, args=args, kwargs=kwargs).start()
