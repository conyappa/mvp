from django.conf import settings
from lottery.models import Draw


numbers = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]


def default(_user):
    return "Lo siento, no sé a qué te refieres."


# In alphabetical order.


def balance(user):
    balance = user.balance
    number_of_tickets = user.number_of_tickets
    msg = f"Tu saldo actual es de *${balance}*, lo que equivale a *{number_of_tickets} boletos*."
    if number_of_tickets < settings.MAX_TICKETS:
        money_for_next_ticket = settings.TICKET_COST - (balance % settings.TICKET_COST)
        msg += (
            f" ¡Deposita ${money_for_next_ticket} para tener {number_of_tickets + 1} "
            "y aumentar tus probabilidades de ganar! 🍀"
        )
    return msg


def deposit(_user):
    msg = (
        ("Ups 🙊... No estamos aceptando depósitos en este momento.")
        if (settings.BANK_ACCOUNT is None)
        else ("Deposítanos a la siguiente cuenta bancaria:\n\n" f"{settings.BANK_ACCOUNT}")
    )
    return msg


# def greeting(_user):
#     msg = (
#         "¡Bienvenido a ConYappa, una lotería que te premia por ahorrar! 💰💰\n"
#         "Mi nombre es YappaBot y seré tu asistente personal."
#     )
#     return msg


def help_(_user):
    msg = (
        "Los comandos disponibles son:\n\n"
        "*boletos*: Revisa cuáles son tus boletos de esta semana 🎟️\n\n"
        "*depositar*: Deposítanos tus ahorros para obtener más boletos 🍀\n\n"
        "*premios*: Mira cuáles son los premios disponibles 👀\n\n"
        "*reglas*: Échale un vistazo a las reglas 📜\n\n"
        "*resultados*: Entérate los números ganadores de esta semana 🎰\n\n"
        "*retirar*: Retira tu dinero a una cuenta bancaria 😢\n\n"
        "*saldo*: Consulta tu saldo actual 💲"
    )
    return msg


def prizes(_user):
    formatted_prizes = "\n".join(
        map(lambda number, prize: f"{number}: {prize}", numbers[0 : len(settings.PRIZES)], settings.PRIZES)
    )
    msg = f"Los premios por cada acierto son:\n\n{formatted_prizes}"
    return msg


def rules(_user):
    msg = (
        f"\nPor cada *${settings.TICKET_COST}* que tengas ahorrados te regalaremos"
        "un boleto para participar en nuestra lotería semanal. 🎁\n\n"
        f"Cada día a las {settings.FORMATTED_DRAW_RESULTS_TIME} saldrá un nuevo número"
        "\n\n¡Mientras más aciertos tenga tu boleto, más ganas! 🤑"
    )
    return msg


def results(user):
    msg = (
        "Los números de esta semana son:\n\n"
        f"{Draw.objects.current().formatted_results}"
        f"\n\n¡Por ahora has ganado *${user.current_prize}*! 💰💰"
    )
    return msg


def tickets(user):
    tickets = user.current_tickets
    if tickets.exists():
        formatted_tickets = "\n".join(
            map(
                lambda number, ticket: f"{number}{' ' * 6}{ticket.formatted_picks}",
                numbers[1 : len(tickets) + 1],
                tickets,
            )
        )
        msg = f"Tus boletos de esta semana son:\n\n{formatted_tickets}"
    else:
        msg = "No tienes boletos esta semana 😢"
    return msg


def withdraw(_user):
    msg = ""
    return msg


handlers = {
    "ayuda": help_,
    "boletos": tickets,
    "depositar": deposit,
    "premios": prizes,
    "reglas": rules,
    "resultados": results,
    "retirar": withdraw,
    "saldo": balance,
}
