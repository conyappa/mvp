from logging import getLogger
import threading as th
from django.conf import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from .. import common_handlers
from .handlers import handlers
from .decorators import adapter


logger = getLogger(__name__)


def setup_webhook(updater):
    webhook_url_base = f"https://{settings.TELEGRAM_WEBHOOK_DOMAIN}:{settings.TELEGRAM_WEBHOOK_PORT}/"
    webhook_url_path = f"bot/telegram/{settings.TELEGRAM_TOKEN}"
    updater.start_webhook(port=settings.TELEGRAM_WEBHOOK_PORT, url_path=webhook_url_path)
    updater.bot.set_webhook(url=webhook_url_base + webhook_url_path)


def boot_updater():
    updater = Updater(token=settings.TELEGRAM_TOKEN)
    dp = updater.dispatcher

    # Simple commands.
    for command, handler in common_handlers.commands.items():
        dp.add_handler(CommandHandler(command, adapter()(handler)))

    # Complex commands.
    for handler in handlers:
        dp.add_handler(handler)

    # Default callback for texts. Add this handler last.
    dp.add_handler(MessageHandler(Filters.text, adapter()(common_handlers.default)))

    if settings.TELEGRAM_WEBHOOK_DOMAIN is None:
        th.Thread(target=updater.start_polling, daemon=True).start()
    else:
        setup_webhook(updater)
