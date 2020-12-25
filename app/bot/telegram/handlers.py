# from telegram.constants import PARSEMODE_MARKDOWN
from accounts.models import User


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

    # if created:
    #     new_user_msg = (
    #         "¡Nuevo usuario! 🎉"
    #         f"\n\nUsername: {user.username}"
    #         f"\n\nNombre: {user.full_name}"

    #     )
    #     context.bot.send_message(chat_id=user.telegram_id, text=msg_body, parse_mode=PARSEMODE_MARKDOWN)
