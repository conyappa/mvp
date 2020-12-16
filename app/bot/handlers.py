import itertools
import datetime as dt
from django.conf import settings
from lottery.models import Draw


numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
weekdays = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
weekdays = weekdays[settings.NEW_DRAW_WEEKDAY :] + weekdays[: settings.NEW_DRAW_WEEKDAY]


def greeting(_user):
    msg = (
        "¡Bienvenido a ConYappa, una lotería que te premia por ahorrar! 💰💰\n"
        "Mi nombre es YappaBot y seré tu asistente personal."
    )
    return msg


def rules(_user):
    formatted_time = dt.time(hour=settings.DRAW_RESULTS_HOUR, minute=settings.DRAW_RESULTS_MINUTE).isoformat(
        timespec="minutes"
    )
    msg = (
        f"\nPor cada *${settings.TICKET_COST}* que tengas ahorrados te regalaremos",
        "un boleto para participar en nuestra lotería semanal. 🎁\n\n",
        f"Cada día a las {formatted_time} saldrá un nuevo número",
        "\n\n¡Mientras más aciertos tenga tu boleto, más ganas! 🤑",
    )
    return msg


def help(_user):
    msg = (
        "Los comandos disponibles son:\n\n"
        "*rules*: Échale un vistazo a las reglas 📜\n"
        "*balance*: Consulta tu saldo actual 💲\n"
        "*deposit*: Deposítanos tus ahorros para obtener más boletos 🍀\n"
        "*results*: Enterate los números ganadores de esta semana 🎰\n"
        "*tickets*: Revisa cuáles son tus boletos de esta semana 🎟️"
    )
    return msg


def balance(user):
    balance = user.balance
    number_of_tickets = user.number_of_tickets
    msg = f"Tu saldo actual es de *${balance}*, lo que equivale a *{number_of_tickets} boletos*."
    if number_of_tickets < settings.MAX_TICKETS:
        money_for_next_ticket = settings.TICKET_COST - (balance % settings.TICKET_COST)
        msg += (
            f" ¡Deposita ${money_for_next_ticket} para tener {number_of_tickets + 1}"
            "y aumentar tus probabilidades de ganar!"
        )
    return msg


def deposit(_user):
    msg = f"Aquí es a donde debes transferir."
    return msg


def results(user):
    draw_results = Draw.objects.current().results
    draw_results += itertools.repeat("?", 7 - len(draw_results))
    formatted_results = "\n".join(map(lambda day, res: f"{day}: {res}", weekdays, draw_results))
    msg = (
        "Los números de esta semana son:\n\n"
        f"{formatted_results}"
        f"\n\n¡Por ahora has ganado *${user.current_prize}*! 💰💰"
    )
    return msg


def tickets(user):
    draw_results = Draw.objects.current().results
    format_ticket = lambda x: ", ".join(map(lambda y: f"*{y}*" if (y in draw_results) else str(y), x.picks))
    tickets = user.current_tickets
    if tickets.exists():
        formatted_tickets = "\n".join(
            map(lambda num, tic: f"{num}{' ' * 6}{format_ticket(tic)}", numbers[0 : len(tickets)], tickets)
        )
        msg = f"Tus boletos de esta semana son:\n\n{formatted_tickets}"
    else:
        msg = "No tienes boletos esta semana 😢"
    return msg


def prizes(_user):
    formatted_prizes = "\n".join(map(lambda n, x: f"{n}: {x}", numbers[0 : len(settings.PRIZES)], settings.PRIZES))
    msg = "Los premios por cada acierto son:\n\n" f"{formatted_prizes}"
    return msg
