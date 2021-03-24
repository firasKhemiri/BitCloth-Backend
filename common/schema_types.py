import graphene

from graphene_django import DjangoObjectType

from common.models import CommentReaction
from post.models import Post, PostReaction, PostImage, PostComment


class CommentReactionType(DjangoObjectType):
    class Meta:
        model = CommentReaction


class CommentType(DjangoObjectType):
    class Meta:
        model = PostComment
    id = graphene.Int()

    reactions = graphene.List(CommentReactionType)

    def resolve_reactions(self, info):
        return self.reactions.all()


class CommentInput(graphene.InputObjectType):
    content = graphene.String(required=True)
