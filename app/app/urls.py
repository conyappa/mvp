from django.urls import path, include
from graphene_django.views import GraphQLView
from . import views


urlpatterns = [
    path("bot/", include("bot.urls")),
    path("graphql", GraphQLView.as_view(graphiql=True)),
    path("admin", views.admin_site.urls),
    path("exception", views.trigger_exception),
    path("", views.landing),
    path("investors", views.investors),
]
