from logging import getLogger
import ast
import json
from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import ConversationHandler
from .decorators import adapter, save_contact, send_contact_to_staff


logger = getLogger(__name__)


STATE_NAMES = (
    "SUPPORT__QUERY",
    "SUPPORT__CONTACT",
    "WITHDRAW__AMOUNT",
    "WITHDRAW__VALID_AMOUNT",
    "WITHDRAW__CONTACT",
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
        },
        "state": STATES["SUPPORT__QUERY"],
    }


@adapter()
def support__contact(user, update, context):
    context.user_data["support_query"] = update.message.text

    cancel = KeyboardButton(text="Cancelar acción")
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
                f"\n\n*Consulta:* {support_query}"
            ),
        },
        "state": ConversationHandler.END,
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
def withdraw__amount(user, update, context):
    if user.balance > 0:
        return {
            "to_user": {
                "text": f"¿Cuánto deseas retirar? (Tienes ${user.balance})",
            },
            "state": STATES["WITHDRAW__AMOUNT"],
        }

    return {
        "to_user": {
            "text": "No tienes nada para retirar 👀.",
        },
        "state": ConversationHandler.END,
    }


@adapter()
def withdraw__amount_is_nan(user, update, context):
    return {
        "to_user": {
            "text": "⚠️ Ese no es un número válido. Ingresa otro valor:",
        },
        "state": STATES["WITHDRAW__AMOUNT"],
    }


@adapter()
def withdraw__contact(user, update, context):
    amount = int(update.message.text)

    if amount > user.balance:
        return {
            "to_user": {
                "text": "⚠️ Excede máximo. Ingresa otro valor:",
            },
            "state": STATES["WITHDRAW__AMOUNT"],
        }

    context.user_data["withdraw_amount"] = amount

    cancel = KeyboardButton(text="Cancelar acción")
    request_contact = KeyboardButton(text="Enviar información de contacto", request_contact=True)
    keyboard = ReplyKeyboardMarkup(keyboard=[[cancel, request_contact]], resize_keyboard=True, one_time_keyboard=True)

    return {
        "to_user": {
            "text": "Perfecto. Envíame tu información de contacto y alguien te escribirá en breve.",
            "reply_markup": keyboard,
        },
        "state": STATES["WITHDRAW__CONTACT"],
    }


@adapter()
@save_contact
@send_contact_to_staff
def withdraw__done(user, update, context):
    amount = context.user_data["withdraw_amount"]

    return {
        "to_user": {
            "text": "Recibido 👌.",
            "reply_markup": ReplyKeyboardRemove(),
        },
        "to_staff": {
            "text": (
                f"Solicitud de *retiro* 💔.\n\nUsername: {user.username}\nNombre: {user.full_name}"
                f"\n\n*Monto:* ${amount}"
            ),
        },
        "state": ConversationHandler.END,
    }


@adapter()
def withdraw__cancel(user, update, context):
    return {
        "to_user": {
            "text": "¡Genial! A seguir ahorrando 💸.",
            "reply_markup": ReplyKeyboardRemove(),
        },
        "state": ConversationHandler.END,
    }


commands = {
    "echo": echo,
    "error": error,
    "start": start,
}
