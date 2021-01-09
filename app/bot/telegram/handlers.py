import logging
import ast
import json
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from .decorators import adapter, save_contact


logger = logging.getLogger(__name__)


DEFAULT_FALLBACK_MSG = "Cancelar"
DEFAULT_FALLBACK_HANDLER = lambda *args, **kwargs: ConversationHandler.END

STATE_NAMES = ("SUPPORT_RECEIVE_CONTACT",)
STATES = dict(zip(STATE_NAMES, range(len(STATE_NAMES))))


# In alphabetical order.


@adapter
def echo(user, update, context):
    parsed_update = ast.literal_eval(str(update))
    update_as_json = json.dumps(parsed_update, indent=4)

    return {
        "to_user": {
            "text": update_as_json,
            "parse_mode": None,
        }
    }


@adapter
def error(user, update, context):
    raise Exception("This is just a test.")


@adapter
@save_contact
def confirm_support(user, update, context):
    return {
        "to_user": {
            "text": "Recibido 👌.",
            "reply_markup": ReplyKeyboardRemove(),
        },
        "to_staff": {
            "text": f"Solicitud de *soporte* 🙄.\n\nUsername: {user.username}\nNombre: {user.full_name}",
            "contact": user.telegram_contact,
        },
        "next_state": ConversationHandler.END,
    }


@adapter
def start(user, update, context):
    return {
        "to_user": {
            "text": (
                "¡Bienvenido a *ConYappa*, una lotería que te premia por ahorrar! 💰💰\n\n"
                "Mi nombre es YappaBot y seré tu asistente personal. "
                "Haz click en /reglas y te explicaré cómo participar."
            )
        }
    }


@adapter
def support(user, update, context):
    cancel = KeyboardButton(text=DEFAULT_FALLBACK_MSG)
    request_contact = KeyboardButton(text="Enviar", request_contact=True)
    keyboard = ReplyKeyboardMarkup(keyboard=[[cancel, request_contact]], resize_keyboard=True, one_time_keyboard=True)

    return {
        "to_user": {
            "text": "Envíame tu información de contacto y le pediré a alguien que te escriba.",
            "reply_markup": keyboard,
        },
        "next_state": STATES["SUPPORT_RECEIVE_CONTACT"],
    }


@adapter
def withdraw(user, update, context):
    if user.balance > 0:
        return {
            "to_user": {
                "text": "Hemos recibido tu solicitud de retiro. ¡Nos pondremos en contacto a la brevedad! 👨‍💻",
            },
            "to_staff": {
                "text": f"Solicitud de *retiro* 💔.\n\nUsername: {user.username}\nNombre: {user.full_name}",
            },
        }

    return {
        "to_user": {
            "text": "No tienes nada para retirar 👀",
        }
    }


commands = {
    "echo": echo,
    "error": error,
    "retirar": withdraw,
    "start": start,
}
