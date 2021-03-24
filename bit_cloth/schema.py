import graphene

from post.schema import (
    Mutation as PostMutation,
    Query as PostQuery
)

from account.schema import (
    Mutation as AccountMutation,
    Query as AccountQuery
)


class Query(
    PostQuery,
    AccountQuery,
):
    pass


class Mutation(
    PostMutation,
    AccountMutation
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
