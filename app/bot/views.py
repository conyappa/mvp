from rest_framework import generics
from rest_framework.response import Response
from . import handlers


# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Bot(generics.GenericAPIView):
    def post(self, request):
        request_msg = request.body.decode()
        handler = getattr(handlers, request_msg, lambda: "Lo siento, no sé a qué te refieres.")
        response_msg = handler()
        return Response(data=response_msg)
