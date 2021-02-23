import graphene
from logging import getLogger
from accounts.views import EmailListEntryType, EmailEntryMutation


logger = getLogger(__name__)


class Query(graphene.ObjectType):
    email_list = graphene.List(EmailListEntryType)

    def resolve_email_list(self, info):
        return EmailListEntryType._meta.model.objects.all()


class Mutation(graphene.ObjectType):
    email_entry = EmailEntryMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
