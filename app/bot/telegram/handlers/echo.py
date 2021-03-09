import ast
import json
from telegram.ext import CommandHandler
from ..decorators import adapter


@adapter()
def echo(user, update, context):
    parsed_update = ast.literal_eval(str(update))
    update_as_json = json.dumps(parsed_update, indent=4)

    return {
        "to_user": {
            "text": update_as_json,
            "parse_mode": None,
        }
    }


handler = CommandHandler("echo", echo)
