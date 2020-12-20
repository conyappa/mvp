from django.urls import path
from . import twilio


app_name = "bot"


urlpatterns = [path("twilio", twilio.replier.ReplierView.as_view())]
