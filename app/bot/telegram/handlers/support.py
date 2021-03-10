from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
from ..decorators import adapter, save_contact, send_contact_to_staff
from ..states import STATES


STATES.register("SUPPORT", "QUERY_REQUESTED")
STATES.register("SUPPORT", "CONTACT_REQUESTED")


@adapter()
def request_query(user, update, context):
    return {
        "to_user": {
            "text": "¿En qué te puedo ayudar? 🤔",
        },
        "state": STATES["SUPPORT", "QUERY_REQUESTED"],
    }


@adapter()
def request_contact(user, update, context):
    context.user_data["support_query"] = update.message.text

    cancel = KeyboardButton(text="Cancelar acción")
    request_contact = KeyboardButton(text="Enviar información de contacto", request_contact=True)
    keyboard = ReplyKeyboardMarkup(keyboard=[[cancel, request_contact]], resize_keyboard=True, one_time_keyboard=True)

    return {
        "to_user": {
            "text": "Perfecto. Envíame tu información de contacto y alguien te escribirá en breve.",
            "reply_markup": keyboard,
        },
        "state": STATES["SUPPORT", "CONTACT_REQUESTED"],
    }


@adapter()
@save_contact
@send_contact_to_staff
def submit(user, update, context):
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
def cancel(user, update, context):
    return {
        "to_user": {
            "text": "Bueno 🙄.",
            "reply_markup": ReplyKeyboardRemove(),
        },
        "state": ConversationHandler.END,
    }


handler = ConversationHandler(
    entry_points=[
        CommandHandler("soporte", request_query),
    ],
    states={
        STATES["SUPPORT", "QUERY_REQUESTED"]: [
            MessageHandler(Filters.text, request_contact),
        ],
        STATES["SUPPORT", "CONTACT_REQUESTED"]: [
            MessageHandler(Filters.contact, submit),
            MessageHandler(Filters.text, cancel),
        ],
    },
    fallbacks=[],
    allow_reentry=True,
)
