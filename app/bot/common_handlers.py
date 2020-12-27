from django.conf import settings
from app.utils import q
from lottery.models import Draw


numbers = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]


def default(user, *args, **kwargs):
    return "Lo siento, no sé a qué te refieres."


# In alphabetical order.


def balance(user, *args, **kwargs):
    balance = user.balance
    number_of_standard_tickets = user.number_of_standard_tickets
    number_of_extra_tickets = user.number_of_extra_tickets

    msg_for_user = (
        f"\nSaldo actual: *${balance}*"
        f"\nGanancias: *${user.winnings}*"
        f"\n\nCon tu saldo actual obtendrás *{q(number_of_standard_tickets, 'boleto')}* en el próximo sorteo"
    )
    msg_for_user += (
        (f" (*+{q(number_of_extra_tickets, 'boleto')}* de regalo 😉).") if (number_of_extra_tickets > 0) else "."
    )

    if number_of_standard_tickets < settings.MAX_TICKETS:
        money_for_next_ticket = settings.TICKET_COST - (balance % settings.TICKET_COST)
        msg_for_user += (
            f"\n\n¡Solo te faltan ${money_for_next_ticket} para obtener otro boleto"
            " y aumentar tus probabilidades de ganar! 🍀"
        )
    return {"msg_for_user": msg_for_user}


def deposit(user, *args, **kwargs):
    msg_for_user = (
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
    return {"msg_for_user": msg_for_user}


def help_(user, *args, **kwargs):
    msg_for_user = (
        "Los comandos disponibles son:"
        "\n\n/boletos: Revisa cuáles son tus boletos de esta semana 🎟️"
        "\n\n/depositar: Deposítanos tus ahorros para obtener más boletos 🍀"
        "\n\n/premios: Mira cuáles son los premios disponibles 👀"
        "\n\n/reglas: Échale un vistazo a las reglas 📜"
        "\n\n/resultados: Entérate los números ganadores de esta semana 🎰"
        "\n\n/retirar: Retira tu dinero a una cuenta bancaria 😢"
        "\n\n/saldo: Consulta tu saldo actual 💲"
    )
    return {"msg_for_user": msg_for_user}


def prizes(user, *args, **kwargs):
    formatted_prizes = "\n".join(
        map(lambda index, prize: f"{numbers[index]}🎯{' ' * 3}...{' ' * 3}*${prize}*", *zip(*enumerate(settings.PRIZES)))
    )
    msg_for_user = (
        "Al finalizar el sorteo,"
        " por cada boleto ganarás un premio de acuerdo con el número de aciertos obtenidos."
        f"\n\n{formatted_prizes}"
    )
    return {"msg_for_user": msg_for_user}


def rules(user, *args, **kwargs):
    msg_for_user = (
        "*ConYappa* es una lotería que te premia por ahorrar 🏆."
        f"\n\nPor cada *${settings.TICKET_COST}* que tengas ahorrados obtendrás"
        " un boleto para participar en nuestro sorteo semanal 🎁,"
        f" que comienza todos los {settings.WEEKDAYS[settings.NEW_DRAW_WEEKDAY]}"
        f" a las {settings.FORMATTED_DRAW_RESULTS_TIME}."
        f"\n\nCada día a la misma hora saldrá un nuevo número."
        " ¡Mientras más aciertos tengas por boleto al finalizar el sorteo, más ganas! 🤑"
        "\n\nEnvía /premios para ver cuánto puedes ganar con cada boleto 💸"
        " o envía /ayuda para conocer los comandos disponibles."
    )
    return {"msg_for_user": msg_for_user}


def results(user, *args, **kwargs):
    msg_for_user = (
        "Los números de esta semana son:"
        f"\n\n{Draw.objects.current().formatted=}"
        f"\n\n¡Envía /boletos para revisar tus aciertos! 🤑"
    )
    return {"msg_for_user": msg_for_user}


def tickets(user, *args, **kwargs):
    tickets = user.current_tickets
    if tickets.exists():
        formatted_tickets = "\n\n".join(
            map(
                lambda index, ticket: f"{numbers[index]}{' ' * 3}...{' ' * 3}{ticket.formatted}",
                *zip(*enumerate(tickets, 1)),
            )
        )
        msg_for_user = (
            f"Tus boletos de esta semana son:\n\n{formatted_tickets}"
            f"\n\n¡Esta semana llevas *${user.current_prize}* ganados! 💰"
        )
    else:
        msg_for_user = "No tienes boletos esta semana 😢."
    return {"msg_for_user": msg_for_user}


commands = {
    "ayuda": help_,
    "boletos": tickets,
    "depositar": deposit,
    "premios": prizes,
    "reglas": rules,
    "resultados": results,
    "saldo": balance,
}
