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


def boot_telegram_updater():
    updater = Updater(settings.TELEGRAM_TOKEN)
    dp = updater.dispatcher

    for command, handler in commands.handlers.items():
        dp.add_handler(CommandHandler(command, handler))
    dp.add_handler(MessageHandler(Filters.text, commands.default))

    th.Thread(target=updater.start_polling, daemon=True).start()
