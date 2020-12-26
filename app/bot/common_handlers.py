from django.conf import settings
from .utils import q
from lottery.models import Draw


numbers = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]


def default(_user):
    return "Lo siento, no sé a qué te refieres."


# In alphabetical order.


def balance(user):
    balance = user.balance
    number_of_standard_tickets = user.number_of_standard_tickets
    number_of_extra_tickets = user.number_of_extra_tickets

    msg = (
        f"\nSaldo actual: *${balance}*"
        f"\nGanancias: *${user.winnings}*"
        f"\n\nCon tu saldo actual obtendrás *{q(number_of_standard_tickets, 'boleto')}* en el próximo sorteo"
    )
    msg += (f" (*+{q(number_of_extra_tickets, 'boleto')}* de regalo 😉).") if (number_of_extra_tickets > 0) else "."

    if number_of_standard_tickets < settings.MAX_TICKETS:
        money_for_next_ticket = settings.TICKET_COST - (balance % settings.TICKET_COST)
        msg += (
            f"\n\n¡Solo te faltan ${money_for_next_ticket} para obtener otro boleto"
            " y aumentar tus probabilidades de ganar! 🍀"
        )
    return msg


def deposit(_user):
    msg = (
        ("Ups 🙊... No estamos aceptando depósitos en este momento.")
        if (settings.BANK_ACCOUNT is None)
        else (
            "Deposítanos a la siguiente cuenta bancaria:"
            f"\n\n{settings.BANK_ACCOUNT}"
            f"\n\nPor ahora tenemos un limite de *${settings.MAX_TICKETS * settings.TICKET_COST}* por persona,"
            " te avisaremos cuando puedas ahorrar más ConYappa 😎"
            "\n\n¡Te hablaremos cuando recibamos tu depósito!"
            )
    )
    return msg


def help_(_user):
    msg = (
        "Los comandos disponibles son:"
        "\n\n/boletos: Revisa cuáles son tus boletos de esta semana 🎟️"
        "\n\n/depositar: Deposítanos tus ahorros para obtener más boletos 🍀"
        "\n\n/premios: Mira cuáles son los premios disponibles 👀"
        "\n\n/reglas: Échale un vistazo a las reglas 📜"
        "\n\n/resultados: Entérate los números ganadores de esta semana 🎰"
        "\n\n/retirar: Retira tu dinero a una cuenta bancaria 😢"
        "\n\n/saldo: Consulta tu saldo actual 💲"
    )
    return msg


def prizes(_user):
    formatted_prizes = "\n".join(
        map(lambda number, prize: f"{number}: {prize} clp", numbers[0 : len(settings.PRIZES)], settings.PRIZES)
    )
    msg = f"Los premios por cada acierto son:\n\n{formatted_prizes}"
    return msg


def rules(_user):
    msg = (
        f"\nPor cada *${settings.TICKET_COST}* que tengas ahorrados obtendrás"
        " un boleto para participar en nuestra lotería semanal 🎁"
        f"\n\nCada día a las {settings.FORMATTED_DRAW_RESULTS_TIME} saldrá un nuevo número."
        " ¡Mientras más aciertos tenga tu boleto, más ganas! 🤑"
        "\n\nEnvía /premios para ver cuánto puedes ganar con cada boleto 💸"
        " o envía /ayuda para saber mas sobre los comandos disponibles."
    )
    return msg


def results(user):
    msg = (
        "Los números de esta semana son:"
        f"\n\n{Draw.objects.current().formatted_results}"
        f"\n\nEnvía /boletos para revisar tus aciertos! 🤑"
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
        msg = (
            f"Tus boletos de esta semana son:\n\n{formatted_tickets}"
            f"\n\n¡Esta semana llevas *${user.current_prize}* ganados! 💰💰"
        )
    else:
        msg = "No tienes boletos esta semana 😢"
    return msg


commands = {
    "ayuda": help_,
    "boletos": tickets,
    "depositar": deposit,
    "premios": prizes,
    "reglas": rules,
    "resultados": results,
    "saldo": balance,
}
