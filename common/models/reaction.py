import enum
from enum import Enum

from django.db import models
from djchoices import DjangoChoices


class ReactionTypes(DjangoChoices):
    LIKE = 1
    HEART = 2
    BRAVO = 3
    AMAZED = 4
    DISLIKE = 5

    # @classmethod
    # def all(self):
    #     return [ReactionTypes.LIKE, ReactionTypes.HEART, ReactionTypes.BRAVO, ReactionTypes.AMAZED,
    #             ReactionTypes.DISLIKE]


class Reaction(models.Model):

    user = models.ForeignKey(to='account.User', on_delete=models.CASCADE, related_name="reactions")

    reaction_type = models.IntegerField(
        choices=[(reaction.value, reaction.name) for reaction in ReactionTypes],
    )

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
