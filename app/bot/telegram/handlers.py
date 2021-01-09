import logging
import ast
import json
from telegram import (
    ForceReply,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    # InlineKeyboardButton,
    # InlineKeyboardMarkup,
)
from telegram.ext import ConversationHandler
from .decorators import adapter, save_contact, send_contact_to_staff


logger = logging.getLogger(__name__)


STATE_NAMES = (
    "SUPPORT__QUERY",
    "SUPPORT__CONTACT",
)
STATES = dict(zip(STATE_NAMES, range(len(STATE_NAMES))))


# In alphabetical order.


@adapter()
def echo(user, update, context):
    parsed_update = ast.literal_eval(str(update))
    update_as_json = json.dumps(parsed_update, indent=4)

    return {
        "to_user": {
            "text": update_as_json,
            "parse_mode": None,
        }
    }


@adapter()
def error(user, update, context):
    raise Exception("This is just a test.")


@adapter()
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


@adapter()
def support__query(user, update, context):
    return {
        "to_user": {
            "text": "¿En qué te puedo ayudar? 🤔",
            "reply_markup": ForceReply(),
        },
        "state": STATES["SUPPORT__QUERY"],
    }


@adapter()
def support__contact(user, update, context):
    context.user_data["support_query"] = update.message.text

    cancel = KeyboardButton(text="Cancelar acción", callback_data=-1)
    request_contact = KeyboardButton(text="Enviar información de contacto", request_contact=True)
    keyboard = ReplyKeyboardMarkup(keyboard=[[cancel, request_contact]], resize_keyboard=True, one_time_keyboard=True)

    return {
        "to_user": {
            "text": "Perfecto. Envíame tu información de contacto y alguien te escribirá en breve.",
            "reply_markup": keyboard,
        },
        "state": STATES["SUPPORT__CONTACT"],
    }


@adapter()
def support__cancel(user, update, context):
    return {
        "to_user": {
            "text": "Bueno 🙄.",
            "reply_markup": ReplyKeyboardRemove(),
        },
        "state": ConversationHandler.END,
    }


@adapter()
@save_contact
@send_contact_to_staff
def support__done(user, update, context):
    support_query = context.user_data.pop("support_query")

    return {
        "to_user": {
            "text": "Recibido 👌.",
            "reply_markup": ReplyKeyboardRemove(),
        },
        "to_staff": {
            "text": (
                f"Solicitud de *soporte* 🙄.\n\nUsername: {user.username}\nNombre: {user.full_name}"
                f"\n\n*Consuta:* {support_query}"
            ),
        },
        "state": ConversationHandler.END,
    }


@adapter()
def withdraw(user, update, context):
    if user.balance > 0:
        return {
            "to_user": {
                "text": "He recibido tu solicitud de retiro. ¡Nos pondremos en contacto a la brevedad! 👨‍💻",
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
