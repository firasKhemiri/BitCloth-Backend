from django.db import models

from common.models.reaction import Reaction


class Comment(models.Model):
    content = models.TextField(max_length=250,)
    user = models.ForeignKey(to='account.User', on_delete=models.CASCADE, related_name="comments")

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class CommentReaction(Reaction):
    comment = models.ForeignKey(to=Comment, blank=True, null=True, on_delete=models.CASCADE, related_name="reactions")
