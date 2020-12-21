from accounts.models import User


def start(update, context):
    telegram_user = update.message.from_user
    username = telegram_user.username or str(telegram_user.id)

    user, _created = User.objects.get_or_create(
        defaults={"username": username, "password": username},
        telegram_id=telegram_user.id,
    )

    user.first_name = telegram_user.first_name or ""
    user.last_name = telegram_user.last_name or ""
    user.save()

    greeting_msg = (
        "¡Bienvenido a ConYappa, una lotería que te premia por ahorrar! 💰💰\n\n"
        "Mi nombre es YappaBot y seré tu asistente personal."
    )
    update.message.reply_text(greeting_msg)
