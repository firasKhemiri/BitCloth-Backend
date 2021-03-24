from django.db import models

from item.models.item import Item
from post.models.post import Post


class Tags(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=255)
    posts = models.ManyToManyField(to=Post, symmetrical=True, related_name="tags")
    items = models.ManyToManyField(to=Item, symmetrical=True, related_name="tags")
