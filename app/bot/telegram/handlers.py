import ast
import json
from accounts.models import User
from . import sender
from .utils import telegram_adapter


# In alphabetical order.


def echo(update, context):
    parsed_update = ast.literal_eval(str(update))
    update_as_json = json.dumps(parsed_update, indent=4)
    update.message.reply_text(update_as_json)


def start(update, context):
    telegram_user = update.message.from_user
    username = telegram_user.username or str(telegram_user.id)

    user, created = User.objects.get_or_create(telegram_id=telegram_user.id, defaults={"username": username})

    user.username = username or user.username
    user.first_name = telegram_user.first_name or user.first_name
    user.last_name = telegram_user.last_name or user.last_name
    user.save()

    greeting_msg = (
        "¡Bienvenido a *ConYappa*, una lotería que te premia por ahorrar! 💰💰\n\n"
        "Mi nombre es YappaBot y seré tu asistente personal. "
        "Envía /reglas y te explicaré cómo participar."
    )
    update.message.reply_markdown(greeting_msg)

    if created:
        new_user_msg = (
            "¡Nuevo usuario! 🎉"
            f"\n\nUsername: {user.username}"
            f"\nNombre: {user.full_name}"
        )
        sender.send_to_staff_group(msg_body=new_user_msg)


def test(update, context):
    pass


@telegram_adapter
def withdraw(user):
    if user.balance:
        withdraw_msg = (
            "Solicitud de retiro 💔"
            f"\n\nUsername: {user.username}"
            f"\nNombre: {user.full_name}"
        )
        sender.send_to_staff_group(msg_body=withdraw_msg)
        msg = "Hemos recibido tu solicitud de retiro. ¡Nos pondremos en contacto a la brevedad! 👨‍💻"
    else:
        msg = "No tienes nada para retirar 🥺"
    return msg


commands = {
    "echo": echo,
    "retirar": withdraw,
    "start": start,
    "test": test,
}
