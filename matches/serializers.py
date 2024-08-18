from rest_framework import serializers

from matches.models import Commander, Match, MatchPlayer, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'favorite_commander',
                  'moxfield_id', 'archidekt_id', 'toski_id']


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
