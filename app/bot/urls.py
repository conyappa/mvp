from django.urls import path
from . import views


app_name = "bot"


urlpatterns = [path("", views.Bot.as_view(), name="respond-to-command")]
