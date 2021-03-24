from typing import Sequence

from django.db.models import Q

from account.models import User
from common.models import Comment
from post.exceptions import InvalidDescriptionValidator
from post.models import Post


def validate_post(user: User, description: str):
    pass



def get_comments_on_post(self, post: Post) -> Sequence[Comment]:
    return Comment.objects.filter(Q(user_id__exact=self.id) and Q(post__exact=post))
