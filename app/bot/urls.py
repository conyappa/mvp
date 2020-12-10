from django.urls import path
from .views import respond_to_command


app_name = "bot"


urlpatterns = [path("", respond_to_command, name="respond-to-command")]
