import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self) -> str:
        return self.username


class Playgroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=15, unique=True)
    owner = models.ForeignKey(
        User, related_name="playgroups_owned", blank=True, on_delete=models.CASCADE
    )
    managers = models.ManyToManyField(
        User, related_name="playgroups_managed", blank=True
    )

    def __str__(self) -> str:
        return self.name


class Player(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    playgroup = models.ForeignKey(
        Playgroup, related_name="players", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("playgroup", "name")

    def __str__(self) -> str:
        return self.name


class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    number_of_turns = models.PositiveSmallIntegerField(blank=True, null=True)
    first_knockout_turn = models.PositiveSmallIntegerField(blank=True, null=True)
    minutes = models.PositiveSmallIntegerField(blank=True, null=True)
    playgroup = models.ForeignKey(
        Playgroup, related_name="matches", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.playgroup.name} match {self.date}"


class Commander(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    color_identity = models.CharField(max_length=5)
    image = models.URLField()
    scryfall_uri = models.URLField()

    def __str__(self) -> str:
        return self.name


class MatchPlayer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rank = models.PositiveSmallIntegerField()
    turn_position = models.PositiveSmallIntegerField()
    commanders = models.ManyToManyField(Commander)
    player = models.ForeignKey(
        Player, related_name="match_players", on_delete=models.PROTECT
    )
    match = models.ForeignKey(
        Match, related_name="match_players", on_delete=models.CASCADE
    )
