from logging import getLogger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, CallbackQueryHandler
from telegram.constants import PARSEMODE_MARKDOWN
from django.core.paginator import Paginator
from accounts.models import User
from ..decorators import adapter
from ..states import STATES


logger = getLogger(__name__)


STATES.register("TICKETS", "DISPLAYED")


numbers = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
page_length = len(numbers[1:])


def tickets(user, update, context, page_num=1):
    tickets = user.current_tickets

    if not tickets.exists():
        return {
            "to_user": {"text": "No tienes boletos esta semana 😢."},
            "state": ConversationHandler.END,
        }

    sorted_tickets = sorted(tickets, key=lambda ticket: ticket.prize, reverse=True)
    paginator = Paginator(object_list=sorted_tickets, per_page=page_length)

    page = paginator.page(page_num)

    formatted_tickets = "\n\n".join(
        map(
            lambda index, ticket: f"{numbers[index]}{' ' * 3}...{' ' * 3}{ticket.formatted}",
            *zip(*enumerate(page, 1)),
        )
    )

    keyboard = [[]]

    if page.has_previous():
        prev_page = InlineKeyboardButton(text="anterior", callback_data=str(page_num - 1))
        keyboard[0].append(prev_page)
    if page.has_next():
        next_page = InlineKeyboardButton(text="siguiente", callback_data=str(page_num + 1))
        keyboard[0].append(next_page)

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

    context.user_data["id"] = user.pk

    return {
        "to_user": {
            "text": (
                f"Tus boletos de esta semana son (pág. {page_num}/{paginator.num_pages}):\n\n{formatted_tickets}"
                f"\n\n¡Esta semana llevas *${user.current_prize}* ganados! 💰"
            ),
            "reply_markup": keyboard,
        },
        "state": STATES["TICKETS", "DISPLAYED"],
    }


@adapter(callback=True)
def change_page(_user, update, context):
    user_id = context.user_data["id"]
    user = User.objects.get(pk=user_id)
    page_num = int(update.data)

    response = tickets(user, update, context, page_num=page_num)
    to_user = response["to_user"]

    update.message.edit_text(text=to_user["text"], parse_mode=PARSEMODE_MARKDOWN)
    update.message.edit_reply_markup(reply_markup=to_user["reply_markup"])

    return {"state": response["state"]}


handler = ConversationHandler(
    entry_points=[
        CommandHandler("boletos", adapter()(tickets)),
    ],
    states={
        STATES["TICKETS", "DISPLAYED"]: [
            CallbackQueryHandler(change_page),
        ],
    },
    fallbacks=[],
    allow_reentry=True,
)
