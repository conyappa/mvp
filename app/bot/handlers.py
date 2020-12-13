import itertools
from django.conf import settings
from lottery.models import Draw


def greeting(_user):
    msg = "¡Bienvenido a ConYapa! Mi nombre es YapaBot y seré tu asistente personal."
    return msg


def help(_user):
    msg = "Los comandos disponilbes son:\nreglas\nsaldo\ndeposito\netc..."
    return msg


def balance(user):
    msg = f"Tu saldo actual es de ${user.balance}, lo que equivale a {user.number_of_tickets} tickets."
    return msg


def deposit(_user):
    msg = f"Aquí es a donde debes transferir."
    return msg


def results(user):
    draw_results = Draw.objects.current().results
    draw_results += itertools.repeat("?", 7 - len(draw_results))
    days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    formatted_results = "\n".join(map(lambda i: f"{days[i]}: {draw_results[i]}", range(7)))
    formatted_prize = f"Por ahora llevas ganado *${user.current_prize}*."
    msg = f"Los números de la semana son:\n\n{formatted_results}\n\n{formatted_prize}"
    return msg


def tickets(user):
    format_ticket = lambda x: ", ".join(map(str, self.picks))
    formatted_tickets = ", ".join(map(format_ticket, user.current_tickets))
    msg = f"Tus tickets de la semana son:\n\n{formatted_tickets}"
    return msg
