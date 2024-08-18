from rest_framework import serializers

from playgroups.models import Commander, Match, MatchPlayer, Player, Playgroup


class PlaygroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playgroup
        fields = ['id', 'name']


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'name']


class CommanderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commander
        fields = ['id', 'name', 'color_identities', 'image', 'scryfall_uri']


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'index', 'date', 'number_of_turns',
                  'first_knockout_turn', 'minutes']


class MatchPlayerSerializer(serializers.ModelSerializer):
    match = MatchSerializer(many=False, read_only=True)
    commanders = CommanderSerializer(many=True, read_only=True)

    class Meta:
        model = MatchPlayer
        fields = ['id', 'name', 'rank', 'turn_position', 'match', 'commanders']
