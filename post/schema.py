import graphene
from graphene import ObjectType

from common.exceptions import AuthenticationError
from post.models import Post
from post.schema_types import PostInput, PostType, StoryType
from post.services import PostServices, get_feed_posts, get_feed_stories


class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        description = graphene.String(required=True)

    def mutate(self, info, description, **kwargs):
        if info.context.user.is_anonymous:
            raise AuthenticationError

        post_data = PostInput()
        post_data.description = description

        post = PostServices().create(post_data, info.context.user)

        return CreatePost(
            post=post
        )


class Mutation(ObjectType):
    create_post = CreatePost.Field()


class Query(ObjectType):
    posts = graphene.List(PostType)
    post = graphene.Field(PostType, post_id=graphene.Int())

    stories = graphene.List(StoryType)

    @staticmethod
    def resolve_posts(root, info):
        if info.context.user.is_anonymous:
            raise Exception('You are not authenticated!')

        return get_feed_posts()
        # else:
        #     return Post.objects.filter(creator=info.context.user)

    @staticmethod
    def resolve_post(self, info, post_id):
        if info.context.user.is_anonymous:
            raise Exception('You are not authenticated!')

        return Post.objects.filter(pk=post_id).first()

    @staticmethod
    def resolve_stories(self, info):
        return get_feed_stories()
