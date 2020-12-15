import inflection
from urllib.parse import parse_qs
from twilio.twiml.messaging_response import MessagingResponse
from rest_framework import generics, status
from django.conf import settings
from django.http import HttpResponse
from accounts.models import User
from . import handlers


# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def use_twilio(view):
    def twilio_view_wrapper(bot, request, *args, **kwargs):
        body = request.body.decode()
        params = {inflection.underscore(k): v[0] for k, v in parse_qs(body).items()}

        if params.get("account_sid") != settings.TWILIO_ACCOUNT_SID:
            return HttpResponse("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
        if "from" not in params:
            return HttpResponse("Bad Request", status=status.HTTP_400_BAD_REQUEST)

        phone = params["from"].strip("whatsapp:")
        user, created = User.objects.get_or_create(defaults={"password": phone}, phone=phone)
        request.twilio_params = {"user": user, "new_user": created, "msg": params.get("body", "")}

        outgoing_msg = view(bot, request, *args, **kwargs)
        response = MessagingResponse()
        response.message().body(outgoing_msg)
        return HttpResponse(content=response, content_type="text/xml")

    return twilio_view_wrapper


class ReplierView(generics.GenericAPIView):
    @use_twilio
    def post(self, request):
        incoming_msg = request.twilio_params["msg"]
        handler = getattr(handlers, incoming_msg.lower(), lambda _user: "Lo siento, no sé a qué te refieres.")
        outgoing_msg = handler(request.twilio_params["user"])
        return outgoing_msg
