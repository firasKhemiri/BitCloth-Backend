import os

from django.db import models


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class Image(models.Model):
    path = models.CharField(max_length=255, blank=False, null=False)
    notes = models.CharField(max_length=25, blank=True, null=True)