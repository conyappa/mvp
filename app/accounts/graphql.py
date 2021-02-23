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


###########
# QUERIES #
###########


class EmailListEntryQuery(graphene.ObjectType):
    email_list_entries = graphene.List(EmailListEntryType)

    def resolve_email_list_entries(self, info):
        return EmailListEntry.objects.all()


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


class EmailListEntryMutation(graphene.ObjectType):
    create_email_list_entry = EmailListEntryCreation.Field()
