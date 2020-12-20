from django.urls import path
from .twilio import replier as twilio_replier


app_name = "bot"


urlpatterns = [path("twilio", twilio_replier.ReplierView.as_view())]
