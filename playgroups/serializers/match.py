from rest_framework import serializers

from playgroups.models import Match, MatchPlayer
from playgroups.serializers.matchplayer import (
    MatchPlayerCreateSerializer,
    MatchPlayerSerializer,
)


class MatchSimpleSerializer(serializers.ModelSerializer):
    playgroup = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Match
        fields = [
            "id",
            "index",
            "date",
            "number_of_turns",
            "first_knockout_turn",
            "minutes",
            "playgroup",
        ]


class MatchSerializer(serializers.ModelSerializer):
    match_players = MatchPlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Match
        fields = [
            "id",
            "index",
            "date",
            "number_of_turns",
            "first_knockout_turn",
            "minutes",
            "match_players",
        ]


class MatchCreateSerializer(serializers.ModelSerializer):
    match_players = MatchPlayerCreateSerializer(many=True, read_only=False)

    class Meta:
        model = Match
        fields = [
            "id",
            "index",
            "date",
            "number_of_turns",
            "first_knockout_turn",
            "minutes",
            "match_players",
        ]
        read_only_fields = ["id", "index"]

    def create(self, validated_data):
        playgroup_id = self.context.get("request").parser_context["kwargs"][
            "playgroup_pk"
        ]
        mp = validated_data.pop("match_players")
        index = Match.objects.filter(playgroup_id=playgroup_id).count() + 1

        match = Match.objects.create(
            index=index, playgroup_id=playgroup_id, **validated_data
        )

        for match_player_data in mp:
            commanders = match_player_data.pop("commanders")
            match_player = MatchPlayer.objects.create(match=match, **match_player_data)
            match_player.commanders.set(commanders)

        return match
