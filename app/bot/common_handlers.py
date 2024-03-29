from logging import getLogger
from django.conf import settings
from app.utils import q
from lottery.models import Draw


logger = getLogger(__name__)


numbers = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]


def simple_response(handler):
    def wrapper(*args, **kwargs):
        msg = handler(*args, **kwargs)
        return {"to_user": {"text": msg}}

    return wrapper


@simple_response
def default(user, *args, **kwargs):
    return "Lo siento, no sé a qué te refieres."


# In alphabetical order.


@simple_response
def balance(user, *args, **kwargs):
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
        money_to_next_ticket = settings.TICKET_COST - (balance % settings.TICKET_COST)
        msg += (
            f"\n\n¡Solo te faltan ${money_to_next_ticket} para obtener otro boleto"
            " y aumentar tus probabilidades de ganar! 🍀"
        )
    return msg


@simple_response
def deposit(user, *args, **kwargs):
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


@simple_response
def help_(user, *args, **kwargs):
    msg = (
        "Los comandos disponibles son:"
        "\n\n/boletos: Revisa cuáles son tus boletos de esta semana 🎟️"
        "\n\n/depositar: Deposítanos tus ahorros para obtener más boletos 🍀"
        "\n\n/premios: Mira cuáles son los premios disponibles 👀"
        "\n\n/reglas: Échale un vistazo a las reglas 📜"
        "\n\n/resultados: Entérate los números ganadores de esta semana 🎰"
        "\n\n/retirar: Retira tu dinero a una cuenta bancaria 😢"
        "\n\n/saldo: Consulta tu saldo actual 💲"
        "\n\n/soporte: ¿Necesitas ayuda con algo?"
    )
    return msg


@simple_response
def prizes(user, *args, **kwargs):
    formatted_prizes = "\n".join(
        map(lambda index, prize: f"{numbers[index]}🎯{' ' * 3}...{' ' * 3}*${prize}*", *zip(*enumerate(settings.PRIZES)))
    )
    msg = (
        "Al finalizar el sorteo,"
        " por cada boleto ganarás un premio de acuerdo con el número de aciertos obtenidos."
        f"\n\n{formatted_prizes}"
    )
    return msg


@simple_response
def rules(user, *args, **kwargs):
    msg = (
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
    return msg


@simple_response
def results(user, *args, **kwargs):
    msg = (
        "Los números de esta semana son:"
        f"\n\n{Draw.objects.current().formatted}"
        f"\n\n¡Envía /boletos para revisar tus aciertos! 🤑"
    )
    return msg


commands = {
    "ayuda": help_,
    "depositar": deposit,
    "premios": prizes,
    "reglas": rules,
    "resultados": results,
    "saldo": balance,
}
