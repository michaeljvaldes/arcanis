import uuid

from django.db import models


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=18)
    favorite_commander = models.UUIDField(
        editable=True, default=None, blank=True, null=True)
    moxfield_id = models.CharField(max_length=50, blank=True, null=True)
    archidekt_id = models.CharField(max_length=50, blank=True, null=True)
    # decks
    toski_id = models.CharField(max_length=50, blank=True, null=True)
