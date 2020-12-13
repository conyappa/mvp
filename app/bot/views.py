from urllib.parse import parse_qs
from twilio.twiml.messaging_response import MessagingResponse
from rest_framework import generics
from django.http import HttpResponse
from . import handlers


# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def use_twilio(view):
    def wrapper(bot, request, *args, **kwargs):
        body = request.body.decode()
        request.twilio = {k: v[0] for k, v in parse_qs(body).items()}
        return view(bot, request, *args, **kwargs)

    return wrapper


class Bot(generics.GenericAPIView):
    @use_twilio
    def post(self, request):
        incoming_text = request.twilio.get("Body", [])
        handler = getattr(handlers, incoming_text.lower(), lambda: "Lo siento, no sé a qué te refieres.")
        outgoing_text = handler()
        response = MessagingResponse()
        response_msg = response.message()
        response_msg.body(outgoing_text)
        return HttpResponse(content=response, content_type="text/xml")
