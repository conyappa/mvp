from .echo import handler as echo
from .error import handler as error
from .start import handler as start
from .support import handler as support
from .tickets import handler as tickets
from .withdraw import handler as withdraw

handlers = {echo, error, start, support, tickets, withdraw}
