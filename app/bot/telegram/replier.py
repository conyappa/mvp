import logging
import threading as th
from django.conf import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from .. import common_handlers
from . import handlers
from .utils import telegram_adapter


logger = logging.getLogger(__name__)


def setup_webhook(updater):
    webhook_url_base = f"https://{settings.TELEGRAM_WEBHOOK_DOMAIN}:{settings.TELEGRAM_WEBHOOK_PORT}/"
    webhook_url_path = f"bot/telegram/{settings.TELEGRAM_TOKEN}"
    updater.start_webhook(port=settings.TELEGRAM_WEBHOOK_PORT, url_path=webhook_url_path)
    updater.bot.set_webhook(url=webhook_url_base + webhook_url_path)


def boot_updater():
    updater = Updater(token=settings.TELEGRAM_TOKEN)
    dp = updater.dispatcher

    for command, handler in common_handlers.commands.items():
        dp.add_handler(CommandHandler(command, telegram_adapter(handler)))

    for command, handler in handlers.commands.items():
        dp.add_handler(CommandHandler(command, handler))

    dp.add_handler(MessageHandler(Filters.text, telegram_adapter(common_handlers.default)))

    if settings.TELEGRAM_WEBHOOK_DOMAIN is None:
        th.Thread(target=updater.start_polling, daemon=True).start()
    else:
        setup_webhook(updater)
