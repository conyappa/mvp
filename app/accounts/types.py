from graphene_django import DjangoObjectType
from .models import User


class EmailListEntryType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("email", "id")
