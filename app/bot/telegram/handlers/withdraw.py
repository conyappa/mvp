from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
from ..decorators import adapter, save_contact, send_contact_to_staff
from ..states import STATES


STATES.register("WITHDRAW", "AMOUNT_REQUESTED")
STATES.register("WITHDRAW", "CONTACT_REQUESTED")


@adapter()
def request_amount(user, update, context):
    if user.balance > 0:
        return {
            "to_user": {
                "text": f"¿Cuánto deseas retirar? (Tienes ${user.balance})",
            },
            "state": STATES["WITHDRAW", "AMOUNT_REQUESTED"],
        }

    return {
        "to_user": {
            "text": "No tienes nada para retirar 👀.",
        },
        "state": ConversationHandler.END,
    }


@adapter()
def request_contact(user, update, context):
    amount = int(update.message.text)

    if amount > user.balance:
        return {
            "to_user": {
                "text": "⚠️ Excede máximo. Ingresa otro valor:",
            },
            "state": STATES["WITHDRAW", "AMOUNT_REQUESTED"],
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
        "state": STATES["WITHDRAW", "CONTACT_REQUESTED"],
    }


@adapter()
def amount_is_nan(user, update, context):
    return {
        "to_user": {
            "text": "⚠️ Ese no es un número válido. Ingresa otro valor:",
        },
        "state": STATES["WITHDRAW", "AMOUNT_REQUESTED"],
    }


@adapter()
@save_contact
@send_contact_to_staff
def submit(user, update, context):
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
def cancel(user, update, context):
    return {
        "to_user": {
            "text": "¡Genial! A seguir ahorrando 💸.",
            "reply_markup": ReplyKeyboardRemove(),
        },
        "state": ConversationHandler.END,
    }


handler = ConversationHandler(
    entry_points=[
        CommandHandler("retirar", request_amount),
    ],
    states={
        STATES["WITHDRAW", "AMOUNT_REQUESTED"]: [
            MessageHandler(Filters.regex(r"^[0-9]+$"), request_contact),
            MessageHandler(Filters.text, amount_is_nan),
        ],
        STATES["WITHDRAW", "CONTACT_REQUESTED"]: [
            MessageHandler(Filters.contact, submit),
            MessageHandler(Filters.text, cancel),
        ],
    },
    fallbacks=[],
    allow_reentry=True,
)
