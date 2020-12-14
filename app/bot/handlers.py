import itertools
from django.conf import settings
from lottery.models import Draw


def greeting(_user):
    msg = "¡Bienvenido a ConYapa! Mi nombre es YapaBot y seré tu asistente personal."
    return msg


def rules(_user):
    msg = "Esta es una lotería que te premia por ahorrar!! 💰"
    msg += f"\nPor cada ${settings.TICKET_COST} que tengas ahorrado te daremos un ticket para participar en nuestra lotería semanal. 🎁"
    msg += f"\n\nCada día a las {settings.DRAW_RESULTS_HOUR}:{settings.DRAW_RESULTS_MINUTE} saldrá un nuevo número."
    msg += "\n\nMientras más aciertos tenga tu ticket, más ganas!! 🤑"
    return msg

def help(_user):
    msg = "Los comandos disponilbes son:\nreglas\nsaldo\ndeposito\netc..."
    return msg


def balance(user):
    msg = f"Tu saldo actual es de *${user.balance}*, lo que equivale a *{user.number_of_tickets} tickets*."
    if user.number_of_tickets < settings.MAX_TICKETS:
        money_for_next_ticket = settings.TICKET_COST - (user.balance % settings.TICKET_COST)
        msg +=  f" ¡Deposita ${money_for_next_ticket} para aumentar tus probabilidades de ganar!"
    return msg


def deposit(_user):
    msg = f"Aquí es a donde debes transferir."
    return msg


def results(user):
    draw_results = Draw.objects.current().results
    draw_results += itertools.repeat("❓", 7 - len(draw_results))
    weekdays = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    formatted_results = "\n".join(map(lambda i: f"{weekdays[i]}: {draw_results[i]}", range(7)))
    formatted_prize = f"¡Por ahora has ganado *${user.current_prize}*! 💰💰"
    msg = f"Los números de esta semana son:\n\n{formatted_results}\n\n{formatted_prize}"
    return msg


def tickets(user):
    draw_results = Draw.objects.current().results
    format_ticket = lambda x: ", ".join(map(lambda y: f"*{y}*" if (y in draw_results) else str(y), x.picks))
    tickets = user.current_tickets
    numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
    formatted_tickets = "\n".join(
        map(lambda n, x: f"{n}{' ' * 6}{format_ticket(x)}", numbers[0 : len(tickets)], tickets)
    )
    msg = (
        f"Tus tickets de esta semana son:\n\n{formatted_tickets}"
        if tickets.exists()
        else "No tienes tickets esta semana 😢"
    )
    return msg
