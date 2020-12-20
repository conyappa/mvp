import logging
import inflection
from urllib.parse import parse_qs
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client as TwilioClient
from twilio.base.exceptions import TwilioRestException
from rest_framework import generics, status
from django.conf import settings
from django.http import HttpResponse
from app.base import BaseSingletone
from app import email
from accounts.models import User
from . import commands


logger = logging.getLogger(__name__)


def use_twilio(view):
    def twilio_view_wrapper(bot, request, *args, **kwargs):
        body = request.body.decode()
        params = {inflection.underscore(k): v[0] for k, v in parse_qs(body).items()}

        try:
            twilio_account_sid = params["account_sid"]
            from_phone = params["from"].split(":")[1]
            to_phone = params["to"].split(":")[1]
        except (KeyError, IndexError):
            return HttpResponse("Bad Request", status=status.HTTP_400_BAD_REQUEST)

        if (twilio_account_sid != settings.TWILIO_ACCOUNT_SID) or (to_phone != settings.TWILIO_PHONE_NUMBER):
            return HttpResponse("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        user, created = User.objects.get_or_create(
            defaults={"username": from_phone, "password": from_phone}, phone=from_phone
        )
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
        handler = commands.handlers.get(incoming_msg.lower(), default=commands.default)
        outgoing_msg = handler(request.twilio_params["user"])
        return outgoing_msg


class SenderClient(BaseSingletone):
    def __init__(self):
        self.twilio_client = TwilioClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    def send(self, users, msg_body_formatter, from_scheme="whatsapp", to_scheme="whatsapp"):
        from_ = f"{from_scheme}:{settings.TWILIO_PHONE_NUMBER}"
        fails = []
        for user in users:
            to = f"{to_scheme}:{user.phone}"
            msg_body = msg_body_formatter(user)
            try:
                self.twilio_client.messages.create(body=msg_body, from_=from_, to=to)
            except TwilioRestException:
                fails.append(user)

        if fails:
            msg_subject_formatter = lambda _user: f"[Twilio] Failed to send SMS from {from_}"
            formatted_users = "\n\n".join(map(str, fails))
            msg_body_formatter = lambda user: (
                f"Hi {user.first_name},\n\n"
                "I wasn't able to send an SMS to the following user(s):\n\n"
                f"{formatted_users}"
            )
            email.SenderClient().send(User.objects.filter(is_staff=True), msg_subject_formatter, msg_body_formatter)
