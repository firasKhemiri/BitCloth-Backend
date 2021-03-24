from django.core.exceptions import ValidationError
from django.db import models

from common.models.comment import Comment
from common.models.image import Image
from common.models.reaction import Reaction
from item.models import Item


class Post(models.Model):
    user = models.ForeignKey('account.User', related_name="posts", on_delete=models.CASCADE)
    description = models.CharField(max_length=250)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    item = models.ForeignKey(to=Item, related_name="posts", on_delete=models.PROTECT, blank=True,null=True)

    @property
    def comments(self):
        return self.comments

    @property
    def log_fields(self):
        return {
            "id": self.id,
            "description": self.description,
            "user": self.user.username,
            "date created": self.date_created,
            "images": self.images,
            "reactions": self.reactions,
            "comments": self.comments,
        }

    def __str__(self):
        return str(self.id)


class PostImage(Image):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")


class PostReaction(Reaction):
    post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.CASCADE, related_name="reactions")

    def validate_unique(self, exclude=None):
        post = Post.objects.filter(id = self.post.id)
        if post.filter(reactions__user = self.user).exists():
            raise ValidationError('Reaction user must be unique')

    def __str__(self):
        return f"Post {self.post.id}, user {self.user_id}"



class PostComment(Comment):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    def clean(self):
        if self.content == "":
            raise ValidationError(self)