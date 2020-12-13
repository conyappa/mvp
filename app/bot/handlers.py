from lottery.models import Draw


def greeting(_user):
    msg = "¡Bienvenido a ConYapa! Mi nombre es YapaBot y seré tu asistente personal."
    return msg


def help(_user):
    msg = "Los comandos disponilbes son:\nreglas\nsaldo\ndeposito\netc..."
    return msg


def balance(user):
    msg = f"Tu saldo actual es de ${user.balance}."
    return msg


def deposit(_user):
    msg = f"Aquí es a donde debes transferir."
    return msg


def results(_user):
    draw = Draw.objects.current()
    msg = f"Los números que han salido en el sorteo de esta semana son:\n{draw.results}"
    return msg


def tickets(user):
    msg = "Estos son tus tickets para esta semana:\n1. ####\n2. ####"
    return msg
