import graphene
from accounts.types import EmailListEntryType


class Query(graphene.ObjectType):
    all_email_list_entries = graphene.List(EmailListEntryType)

    def resolve_all_email_list_entries(self, info):
        return EmailListEntryType._meta.model.objects.all()


schema = graphene.Schema(query=Query)
