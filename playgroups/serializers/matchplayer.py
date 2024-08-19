from rest_framework import serializers

from playgroups.models import Commander, Match, MatchPlayer, Player
from playgroups.serializers.commander import CommanderSerializer


class MatchPlayerSerializer(serializers.ModelSerializer):
    match = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, queryset=Match.objects.all())
    player = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, queryset=Player.objects.all())
    commanders = CommanderSerializer(many=True, read_only=True)

    class Meta:
        model = MatchPlayer
        fields = ['id', 'rank', 'turn_position',
                  'match', 'player', 'commanders']


class MatchPlayerCreateSerializer(serializers.ModelSerializer):
    player = serializers.PrimaryKeyRelatedField(
        many=False, queryset=Player.objects.all()
    )
    commanders = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Commander.objects.all()
    )

    class Meta:
        model = MatchPlayer
        fields = ['rank', 'turn_position', 'player', 'commanders']

    def validate_commanders(self, value):
        if len(value) < 1:
            raise serializers.ValidationError(
                "Match player must have at least one commander"
            )
        return value
