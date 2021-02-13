from django.urls import path, include
from . import views


urlpatterns = [
    path("admin", views.admin_site.urls),
    path("exception", views.trigger_exception),
    path("", views.landing_page),
    path("investors", views.landing_page),
    path("bot/", include("bot.urls")),
]
