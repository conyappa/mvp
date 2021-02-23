import graphene
from graphene_django import DjangoObjectType
from .models import EmailListEntry


#########
# TYPES #
#########


class EmailListEntryType(DjangoObjectType):
    class Meta:
        model = EmailListEntry
        fields = ("email",)


#############
# MUTATIONS #
#############


class EmailListEntryCreation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)

    email_list_entry = graphene.Field(EmailListEntryType)

    @classmethod
    def mutate(cls, root, info, email):
        entry = EmailListEntry.objects.create(email=email)
        return EmailListEntryCreation(email_list_entry=entry)
