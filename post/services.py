import logging

from account.models import User
from post.models import Post
from post.models.story import Story
from post.schema_types import PostInput
from post.utils import validate_post

logger = logging.getLogger(__name__)


class PostServices:

    @staticmethod
    def create(post_data: PostInput, user: User):
        # if user.is_authenticated:
        validate_post(user, post_data.description)

        post = Post(
            description=post_data.description,
            user=user,
        )

        post.full_clean()
        post.save()

        logger.info("Created quote in database.", extra={"post": post.log_fields})

        return post


def get_feed_posts():
    posts = Post.objects.all()
    return posts


def get_feed_stories():
    stories = Story.objects.all()
    return stories
