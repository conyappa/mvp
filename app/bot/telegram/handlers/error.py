from telegram.ext import CommandHandler
from ..decorators import adapter


@adapter()
def error(user, update, context):
    raise Exception("This is just a test.")


handler = CommandHandler("error", error)
