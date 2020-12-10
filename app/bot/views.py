from rest_framework import exceptions
from rest_framework.response import Response


# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def only_post(view):
    def wrapper(request, *args, **kwargs):
        if request.method == "POST":
            return view(request, *args, **kwargs)
        return exceptions.MethodNotAllowed()

    return wrapper


@only_post
def respond_to_command(request):
    message = request.body
    logger.error(message)
    return Response()
