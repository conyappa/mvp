from django.apps import AppConfig
from django.conf import settings


class BotConfig(AppConfig):
    name = "bot"

    def ready(_self):
        if settings.TELEGRAM_TOKEN is not None:
            from .telegram import replier

            replier.boot_updater()
