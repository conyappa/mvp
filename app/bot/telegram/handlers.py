import logging
import ast
import json


logger = logging.getLogger(__name__)


# In alphabetical order.


def echo(user, update, context):
    parsed_update = ast.literal_eval(str(update))
    update_as_json = json.dumps(parsed_update, indent=4)
    update.message.reply_text(update_as_json)


def error(user, update, context):
    raise Exception("This is just a test.")


def start(user, update, context):
    response = {}
    response["msg_for_user"] = (
        "¡Bienvenido a *ConYappa*, una lotería que te premia por ahorrar! 💰💰\n\n"
        "Mi nombre es YappaBot y seré tu asistente personal. "
        "Haz click en /reglas y te explicaré cómo participar."
    )
    return response


def withdraw(user, update, context):
    response = {}

    if user.balance > 0:
        response[
            "msg_for_user"
        ] = "Hemos recibido tu solicitud de retiro. ¡Nos pondremos en contacto a la brevedad! 👨‍💻"
        response["msg_for_staff"] = (
            "Solicitud de retiro 💔." f"\n\nUsername: {user.username}" f"\nNombre: {user.full_name}"
        )
    else:
        response["msg_for_user"] = "No tienes nada para retirar 👀"

    return response


commands = {
    "echo": echo,
    "error": error,
    "retirar": withdraw,
    "start": start,
}
