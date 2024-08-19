import uuid

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Playgroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=15)
    owner = models.ForeignKey(
        Profile, related_name='playgroups_owned', null=True, on_delete=models.SET_NULL)
    managers = models.ManyToManyField(
        Profile, related_name='playgroups_managed'
    )

    def __str__(self) -> str:
        return self.name


class Player(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    playgroup = models.ForeignKey(
        Playgroup, related_name='players', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('playgroup', 'name')

    def __str__(self) -> str:
        return self.name


class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    index = models.PositiveIntegerField()
    date = models.DateField()
    number_of_turns = models.PositiveSmallIntegerField(blank=True, null=True)
    first_knockout_turn = models.PositiveSmallIntegerField(
        blank=True, null=True)
    minutes = models.PositiveSmallIntegerField(blank=True, null=True)
    playgroup = models.ForeignKey(
        Playgroup, related_name='matches', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('playgroup', 'index')


class Commander(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    color_identities = models.CharField(max_length=5)
    image = models.URLField()
    scryfall_uri = models.URLField()


class MatchPlayer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rank = models.PositiveSmallIntegerField()
    turn_position = models.PositiveSmallIntegerField()
    commanders = models.ManyToManyField(Commander)
    player = models.ForeignKey(
        Player, related_name='match_players', on_delete=models.CASCADE)
    match = models.ForeignKey(
        Match, related_name='match_players', on_delete=models.CASCADE)
