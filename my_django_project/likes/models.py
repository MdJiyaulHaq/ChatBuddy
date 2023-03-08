from django.db import models
from django.contrib.auth.models import *
from django.contrib.contenttypes import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.


class LikedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(max_length=255)
    content_object = GenericForeignKey()


class User(models.Model):
    item = models.TextField(max_length=255)
