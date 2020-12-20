from django.apps import AppConfig


class BotConfig(AppConfig):
    name = "bot"

    def ready(_self):
        from .telegram import boot_telegram_updater

        boot_telegram_updater()
