import graphene
from logging import getLogger
from accounts.graphql import EmailListEntryType, EmailListEntryCreation


logger = getLogger(__name__)


class Query(graphene.ObjectType):
    all_email_list_entries = graphene.List(EmailListEntryType)

    def resolve_all_email_list_entries(self, info):
        return EmailListEntryType._meta.model.objects.all()


class Mutation(graphene.ObjectType):
    create_email_list_entry = EmailListEntryCreation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
