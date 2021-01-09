import logging
import threading as th
from django.conf import settings
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from .. import common_handlers
from . import handlers
from .handlers import STATES
from .decorators import adapter


logger = logging.getLogger(__name__)


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
    for command, handler in handlers.commands.items():
        dp.add_handler(CommandHandler(command, handler))

    # /support flow.
    dp.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler("soporte", handlers.support__query),
            ],
            states={
                STATES["SUPPORT__QUERY"]: [
                    MessageHandler(Filters.text, handlers.support__contact),
                ],
                STATES["SUPPORT__CONTACT"]: [
                    MessageHandler(Filters.contact, handlers.support__done),
                    MessageHandler(Filters.text, handlers.support__cancel),
                ],
            },
            fallbacks=[],
            allow_reentry=True,
        )
    )

    # /withdraw flow.
    dp.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler("retirar", handlers.withdraw__amount),
            ],
            states={
                STATES["WITHDRAW__AMOUNT"]: [
                    MessageHandler(Filters.regex(r"^[0-9]+$"), handlers.withdraw__contact),
                    MessageHandler(Filters.text, handlers.withdraw__amount_is_nan),
                ],
                STATES["WITHDRAW__CONTACT"]: [
                    MessageHandler(Filters.contact, handlers.withdraw__done),
                    MessageHandler(Filters.text, handlers.withdraw__cancel),
                ],
            },
            fallbacks=[],
            allow_reentry=True,
        )
    )

    # Default callback for texts. Add this handler last.
    dp.add_handler(MessageHandler(Filters.text, adapter()(common_handlers.default)))

    if settings.TELEGRAM_WEBHOOK_DOMAIN is None:
        th.Thread(target=updater.start_polling, daemon=True).start()
    else:
        setup_webhook(updater)
