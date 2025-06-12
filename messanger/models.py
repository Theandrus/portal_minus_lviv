from django.db import models
from django.contrib.auth.models import User


class Channels(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    is_active = models.BooleanField()


class NewMessagesChannels(models.Model):
    count = models.IntegerField(null=True, blank=True)
    frm_user = models.ForeignKey(User, on_delete=models.PROTECT)
    to_user = models.IntegerField()