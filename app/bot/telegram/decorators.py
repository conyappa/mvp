import logging
from telegram.constants import PARSEMODE_MARKDOWN
from django.conf import settings
from accounts.models import User


logger = logging.getLogger(__name__)


class HandlerError(Exception):
    pass


def process_response(handler):
    def wrapper(update, context, callback=False):
        response = handler(update, context, callback) or {}
        to_user = response.get("to_user")
        to_staff = response.get("to_staff")
        exception = response.get("exception")
        state = response.get("state")

        logger.info(update)

        if to_user:
            to_user.setdefault("parse_mode", PARSEMODE_MARKDOWN)
            context.bot.send_message(
                chat_id=update.message.chat.id,
                reply_to_message_id=update.message.message_id,
                allow_sending_without_reply=True,
                **to_user,
            )

        if to_staff:
            to_staff.setdefault("parse_mode", PARSEMODE_MARKDOWN)
            context.bot.send_message(chat_id=settings.TELEGRAM_STAFF_GROUP_ID, **to_staff)

        if exception:
            msg = exception.get("msg")
            raise exception["obj"](msg)

        if state is not None:
            return state

    return wrapper


def report_exception(handler):
    def wrapper(user, update, context):
        try:
            return handler(user, update, context)
        except Exception as exception:
            exception_msg = f"{type(exception).__name__}: {exception}"
            return {
                "to_user": {
                    "text": "¡Oh no! Ha ocurrido un error 😓. Vuelve a intentarlo más tarde.",
                },
                "to_staff": {
                    "text": (
                        "¡Ha ocurrido un error! 🚨"
                        f"\n\nUsername: {user.username}"
                        f"\nNombre: {user.full_name}"
                        f"\nMensaje: {update.message.text or ''}"
                        f"\n\n`{exception_msg}`"
                    ),
                },
                "exception": {
                    "obj": HandlerError,
                    "msg": exception_msg,
                },
            }

    return wrapper


def use_user(handler):
    def wrapper(update, context, callback=False):
        telegram_user = update.from_user if callback else update.message.from_user

        try:
            user = User.objects.get(telegram_id=telegram_user.id)
            created = False
        except User.DoesNotExist:
            makeshift_username = telegram_user.username or str(telegram_user.id)
            user = User.objects.create(telegram_id=telegram_user.id, username=makeshift_username)
            created = True

        user.username = telegram_user.username or user.username
        user.first_name = telegram_user.first_name or user.first_name
        user.last_name = telegram_user.last_name or user.last_name
        user.save()

        if created:
            context.bot.send_message(
                chat_id=settings.TELEGRAM_STAFF_GROUP_ID,
                text="¡Nuevo usuario! 🎉" f"\n\nUsername: {user.username}" f"\nNombre: {user.full_name}",
            )

        return handler(user, update, context)

    return wrapper


def adapter(callback=False):
    def inner(handler):
        def wrapper(update, context):
            decorated_handler = process_response(use_user(report_exception(handler)))
            return decorated_handler(update.callback_query if callback else update, context, callback)

        return wrapper

    return inner


def save_contact(handler):
    def wrapper(user, update, context):
        contact = update.message.contact
        user.phone = contact.phone_number
        user.save()
        return handler(user, update, context)

    return wrapper


def send_contact_to_staff(handler):
    def wrapper(user, update, context):
        response = handler(user, update, context)
        contact = user.telegram_contact
        context.bot.send_contact(chat_id=settings.TELEGRAM_STAFF_GROUP_ID, contact=contact)
        return response

    return wrapper
