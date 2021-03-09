from telegram.ext import CommandHandler
from ..decorators import adapter


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


handler = CommandHandler("start", start)
