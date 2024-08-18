import uuid

from django.db import models


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    favorite_commander = models.UUIDField(
        editable=True, default=None, blank=True, null=True)
    moxfield_id = models.CharField(max_length=50, blank=True, null=True)
    archidekt_id = models.CharField(max_length=50, blank=True, null=True)
    # decks
    toski_id = models.CharField(max_length=50, blank=True, null=True)

    user = models.ForeignKey(
        'auth.User', related_name='profiles', on_delete=models.CASCADE)


class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    index = models.PositiveIntegerField()
    date = models.DateField()
    number_of_turns = models.PositiveSmallIntegerField(blank=True, null=True)
    first_knockout_turn = models.PositiveSmallIntegerField(
        blank=True, null=True)
    minutes = models.PositiveSmallIntegerField(blank=True, null=True)


class Commander(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    color_identities = models.CharField(max_length=5)
    image = models.URLField()
    scryfall_uri = models.URLField()


class MatchPlayer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    rank = models.PositiveSmallIntegerField()
    turn_position = models.PositiveSmallIntegerField()
    commanders = models.ManyToManyField(Commander)
    match = models.ForeignKey(
        Match, related_name='match_players', on_delete=models.CASCADE)
