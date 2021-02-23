import graphene
from logging import getLogger
from accounts.graphql import EmailListEntryQuery, EmailListEntryMutation


logger = getLogger(__name__)


class Query(EmailListEntryQuery, graphene.ObjectType):
    pass


class Mutation(EmailListEntryMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
