from django.core.exceptions import ValidationError
from django.db import models
from djchoices import DjangoChoices, ChoiceItem

from common.models.comment import Comment
from common.models.image import Image
from common.models.reaction import Reaction


class Item(models.Model):
    class Availability(DjangoChoices):
        UNAVAILABLE = ChoiceItem(0)
        AVAILABLE = ChoiceItem(1)

    user = models.ForeignKey('account.User', related_name="items", on_delete=models.CASCADE)

    name = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=5, decimal_places=1, null=False, blank=False)

    color = models.CharField(max_length=25)
    options = models.CharField(max_length=25)

    type = models.CharField(max_length=25)
    state = models.IntegerField(choices=Availability.choices)

    discount = models.DecimalField(max_digits=5, decimal_places=1,null=True,blank=True)


    def clean(self):
        if self.discount:
            if self.discount >= self.price:
                raise ValidationError("Discount can't be higher than price.")


class ItemReaction(Reaction):
    item = models.ForeignKey(to=Item, blank=True, null=True, on_delete=models.CASCADE, related_name="reactions")


class ItemComments(Comment):
    item = models.ForeignKey(to=Item, on_delete=models.CASCADE, related_name="comments")


class ItemImage(Image):
    item = models.ForeignKey(to=Item, on_delete=models.CASCADE, related_name="images")



