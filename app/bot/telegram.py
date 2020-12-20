import logging
import threading as th
from django.conf import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from . import commands


logger = logging.getLogger(__name__)


def use_telegram(handler):
    def telegram_handler_wrapper(update, context):
        logger.error(update)
        logger.error(context)
        update.message.reply_text("test answer")

    return telegram_handler_wrapper


def setup_webhook(updater):
    webhook_url_base = f"{settings.TELEGRAM_WEBHOOK_URL}:{settings.TELEGRAM_WEBHOOK_PORT}/"
    webhook_url_path = f"bot/telegram/{settings.TELEGRAM_TOKEN}"
    updater.start_webhook(listen="localhost", port=settings.TELEGRAM_WEBHOOK_PORT, url_path=webhook_url_path)
    updater.bot.set_webhook(url=webhook_url_base + webhook_url_path)


def boot_telegram_updater():
    updater = Updater(settings.TELEGRAM_TOKEN)
    dp = updater.dispatcher

    for command, handler in commands.handlers.items():
        dp.add_handler(CommandHandler(command, use_telegram(handler)))
    dp.add_handler(MessageHandler(Filters.text, use_telegram(commands.default)))

    if settings.TELEGRAM_WEBHOOK_DOMAIN is not None:
        setup_webhook(updater)
    else:
        th.Thread(target=updater.start_polling, daemon=True).start()
