import inflection
from urllib.parse import parse_qs
from twilio.twiml.messaging_response import MessagingResponse
from rest_framework import generics
from django.http import HttpResponse
from accounts.models import User
from . import handlers


# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def use_twilio(view):
    def wrapper(bot, request, *args, **kwargs):
        body = request.body.decode()
        params = {inflection.underscore(k): v[0] for k, v in parse_qs(body).items()}
        phone = params["from"].strip("whatsapp:")

        user, created = User.objects.get_or_create(
            defaults={"phone": phone, "password": phone}, twilio_account_sid=params["account_sid"]
        )
        request.twilio_params = {"user": user, "new_user": created, "msg": params["body"]}

        outgoing_msg = view(bot, request, *args, **kwargs)
        response = MessagingResponse()
        response.message().body(outgoing_msg)
        return HttpResponse(content=response, content_type="text/xml")

    return wrapper


class Bot(generics.GenericAPIView):
    @use_twilio
    def post(self, request):
        incoming_msg = request.twilio_params["msg"]
        handler = getattr(handlers, incoming_msg.lower(), lambda: "Lo siento, no sé a qué te refieres.")
        outgoing_msg = handler(request.twilio_params["user"])
        return outgoing_msg
