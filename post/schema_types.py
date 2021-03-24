import graphene
from graphene_django import DjangoObjectType

from common.models import Reaction
from common.models.reaction import ReactionTypes
from common.schema_types import CommentType
from post.models import Post, PostReaction, PostImage
from post.models.story import Story, StoryImage, StoryReaction


class ReactionType(DjangoObjectType):
    class Meta:
        model = PostReaction
        convert_choices_to_enum = False
    id = graphene.Int()
    # type = graphene.Int()
    # typeOfReaction = graphene.String

    # reactionType = Reaction.ReactionTypes
    # reactionType = ReactionTypes
    convert_choices_to_enum = ["reactionType"]


class ImageType(DjangoObjectType):
    class Meta:
        model = PostImage
    id = graphene.Int()


class PostType(DjangoObjectType):
    class Meta:
        model = Post

    id = graphene.Int()
    reactions = graphene.List(ReactionType)
    images = graphene.List(ImageType)
    comments = graphene.List(CommentType)
    comment_count = graphene.Int()

    def resolve_comment_count(self, info):
        return self.comments.count()

    def resolve_images(self, info):
        return self.images.all()

    def resolve_reactions(self, info):
        return self.reactions.all()

    def resolve_comments(self, info):
        return self.comments.all()


class PostInput(graphene.InputObjectType):
    description = graphene.String(required=True)


class StoryImageType(DjangoObjectType):
    class Meta:
        model = StoryImage
    id = graphene.Int()


class StoryReactionType(DjangoObjectType):
    class Meta:
        model = StoryReaction
    id = graphene.Int()


#
# class StoryStickerType(DjangoObjectType):
#     class Meta:
#         model = StorySticker


class StoryType(DjangoObjectType):
    class Meta:
        model = Story

    id = graphene.Int()
    reactions = graphene.List(StoryReactionType)
    image = graphene.Field(StoryImageType)
    comments = graphene.List(CommentType)

    def resolve_image(self, info):
        return self.image

    def resolve_reactions(self, info):
        return self.reactions.all()

    def resolve_comments(self, info):
        return self.comments.all()
