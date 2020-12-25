from accounts.models import User


def telegram_adapter(handler):
    def wrapper(update, context):
        telegram_user = update.message.from_user

        try:
            user = User.objects.get(telegram_id=telegram_user.id)
        except User.DoesNotExist:
            update.message.reply_text("¡No nos hemos presentado! Envía /start para comenzar.")
        else:
            user.username = telegram_user.username or user.username
            user.first_name = telegram_user.first_name or user.first_name
            user.last_name = telegram_user.last_name or user.last_name
            user.save()

            msg = handler(user)
            update.message.reply_markdown(msg)

    return wrapper
