from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("admin", admin.site.urls),
    path("exception", views.trigger_exception),
    path("bot", include("bot.urls")),
]
