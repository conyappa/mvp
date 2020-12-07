from django.urls import path, include
from . import views


urlpatterns = [
    path("exception/", views.trigger_exception),
    path("", include("accounts.urls")),
    path("", include("lottery.urls")),
]
