from django.urls import path
from .views import Bot


app_name = "bot"


urlpatterns = [path("", Bot.as_view(), name="respond-to-command")]
