from django.urls import path
from . import twilio


app_name = "bot"


urlpatterns = [path("", twilio.ReplierView.as_view())]
