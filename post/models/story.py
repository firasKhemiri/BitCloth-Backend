from django.core.exceptions import ValidationError
from django.db import models
from djchoices import DjangoChoices, ChoiceItem

from common.models.comment import Comment
from common.models.image import Image
from common.models.reaction import Reaction
from item.models import Item


class Story(models.Model):
    user = models.ForeignKey('account.User', related_name="stories", on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    item = models.ForeignKey(to=Item, related_name="stories", on_delete=models.PROTECT, blank=True, null=True)

    @property
    def log_fields(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "date created": self.date_created,
            "images": self.image,
            "reactions": self.reactions,
            "comments": self.comments,
            "story": self.stickers
        }

    def __str__(self):
        return str(self.id)


class StoryImage(Image):
    story = models.OneToOneField(Story, on_delete=models.CASCADE, related_name="image")


class StoryReaction(Reaction):
    story = models.ForeignKey(Story, blank=True, null=True, on_delete=models.CASCADE, related_name="reactions")

    def __str__(self):
        return f"Post {self.story.id}, user {self.user_id}"


class StoryComment(Comment):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="comments")

    def clean(self):
        if self.content == "":
            raise ValidationError(self)


class StorySticker(models.Model):
    class StickerTypes(DjangoChoices):
        TEXT = ChoiceItem(0)
        STICKER = ChoiceItem(1)
        GIF = ChoiceItem(2)

    type = models.CharField(choices=StickerTypes.choices, max_length=8, blank=False, null=False, default=False)

    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="stickers")
    text = models.CharField(max_length=1000, null=True, blank=True)
    gif = models.CharField(max_length=100, null=True, blank=True)

    orientation = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    pos_x = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    pos_y = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    size = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)

    link = models.CharField(max_length=250, null=True, blank=True)
