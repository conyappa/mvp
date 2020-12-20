import logging
import threading as th
from django.conf import settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from accounts.models import User
from .. import common_handlers
from . import handlers


logger = logging.getLogger(__name__)


def telegram_adapter(handler):
    def wrapper(update, context):
        telegram_user = update.message.from_user

        try:
            user = User.objects.get(telegram_id=telegram_user.id)
        except User.DoesNotExist:
            update.message.reply_text("¡No nos hemos presentado! Envía /start para comenzar.")
        else:
            user.first_name = telegram_user.first_name or ""
            user.last_name = telegram_user.last_name or ""
            user.save()
            msg = handler(user)
            update.message.reply_text(msg)

    return wrapper


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

    dp.add_handler(CommandHandler("start", handlers.start))
    dp.add_handler(MessageHandler(Filters.text, telegram_adapter(common_handlers.default)))

    if settings.TELEGRAM_WEBHOOK_DOMAIN is None:
        updater_daemon = th.Thread(target=updater.start_polling, daemon=True)
    else:
        updater_daemon = th.Thread(target=setup_webhook, daemon=True, args=(updater,))

    updater_daemon.start()
