import logging
from telegram.constants import PARSEMODE_MARKDOWN
from . import sender
from accounts.models import User


logger = logging.getLogger(__name__)


class HandlerError(Exception):
    pass


def raise_(msg):
    raise HandlerError(msg)


def process_response(handler):
    def wrapper(update, context):
        response = handler(update, context) or {}

        msg_for_user = response.get("msg_for_user")
        if msg_for_user is not None:
            repliers = {None: update.message.reply_text, PARSEMODE_MARKDOWN: update.message.reply_markdown}
            msg_for_user_parse_mode = response.get("msg_for_user_parse_mode", PARSEMODE_MARKDOWN)
            repliers[msg_for_user_parse_mode](msg_for_user)

        msg_for_staff = response.get("msg_for_staff")
        if msg_for_staff is not None:
            msg_for_staff_parse_mode = response.get("msg_for_staff_parse_mode", PARSEMODE_MARKDOWN)
            sender.send_to_staff_group(msg_body=msg_for_staff, parse_mode=msg_for_staff_parse_mode)

        callback = response.get("callback")
        callback_args = response.get("callback_args", ())
        callback_kwargs = response.get("callback_kwargs", {})
        if callback is not None:
            callback(*callback_args, **callback_kwargs)

    return wrapper


def report_exception(handler):
    def wrapper(user, update, context):
        try:
            return handler(user, update, context)
        except Exception as exception:
            exception_msg = str(exception)
            return {
                "msg_for_user": "¡Oh no! Ha ocurrido un error 😓. Vuelve a intentarlo más tarde.",
                "msg_for_staff": (
                    "¡Ha ocurrido un error! 🚨"
                    f"\n\nUsername: {user.username}"
                    f"\nNombre: {user.full_name}"
                    f"\nMensaje: {update.message.text}"
                    f"\n\n`{type(exception).__name__}: {exception}`"
                ),
                "callback": lambda: raise_(exception_msg),
            }

    return wrapper


def use_user(handler):
    def wrapper(update, context):
        telegram_user = update.message.from_user

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
            sender.send_to_staff_group(
                msg_body="¡Nuevo usuario! 🎉" f"\n\nUsername: {user.username}" f"\nNombre: {user.full_name}"
            )

        return handler(user, update, context)

    return wrapper


def adapter(handler):
    def wrapper(update, context):
        decorated_handler = process_response(use_user(report_exception(handler)))
        return decorated_handler(update, context)

    return wrapper
