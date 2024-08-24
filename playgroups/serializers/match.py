import uuid

from rest_framework import serializers

from playgroups.models import Match, MatchPlayer
from playgroups.serializers.matchplayer import MatchPlayerSerializer


class MatchSerializer(serializers.ModelSerializer):
    match_players = MatchPlayerSerializer(many=True, read_only=False)

    class Meta:
        model = Match
        fields = [
            "id",
            "playgroup",
            "date",
            "number_of_turns",
            "first_knockout_turn",
            "minutes",
            "match_players",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        # ensure the playgroup matches the id in the route
        playgroup_id = uuid.UUID(
            self.context["request"].parser_context["kwargs"]["playgroup_pk"]
        )
        if playgroup_id != attrs["playgroup"].id:
            raise serializers.ValidationError(
                f"Match playgroup id does not match route"
            )
        return attrs

    def create(self, validated_data):
        mp = validated_data.pop("match_players")
        instance = super().create(validated_data)

        for match_player_data in mp:
            commanders = match_player_data.pop("commanders")
            match_player = MatchPlayer.objects.create(
                match=instance, **match_player_data
            )
            match_player.commanders.set(commanders)
        return instance

    def update(self, instance, validated_data):
        mp = validated_data.pop("match_players")
        instance = super().update(instance, validated_data)

        # delete and replace match players
        MatchPlayer.objects.filter(match=instance).delete()
        for match_player_data in mp:
            commanders = match_player_data.pop("commanders")
            match_player = MatchPlayer.objects.create(
                match=instance, **match_player_data
            )
            match_player.commanders.set(commanders)

        return instance
