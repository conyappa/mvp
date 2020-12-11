from twilio.twiml.messaging_response import MessagingResponse
from rest_framework import generics
from django.http import HttpResponse
from . import handlers


# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Bot(generics.GenericAPIView):
    def post(self, request):
        incoming_text = request.body.decode()
        # logger.error(request.values)
        handler = getattr(handlers, incoming_text.lower(), lambda: "Lo siento, no sé a qué te refieres.")
        outgoing_text = handler()
        response = MessagingResponse()
        response_msg = response.message()
        response_msg.body(outgoing_text)
        return HttpResponse(content=response, content_type="text/xml")
