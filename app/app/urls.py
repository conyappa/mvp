from django.urls import path, include
from . import views


urlpatterns = [
    path("sentry-debug/", views.trigger_error),
]
