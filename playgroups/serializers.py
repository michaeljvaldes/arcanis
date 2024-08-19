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


class SimpleMatchSerializer(serializers.ModelSerializer):
    playgroup = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Match
        fields = ['id', 'index', 'date', 'number_of_turns',
                  'first_knockout_turn', 'minutes', 'playgroup']


class MatchSerializer(serializers.ModelSerializer):
    match_players = MatchPlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Match
        fields = ['id', 'index', 'date', 'number_of_turns',
                  'first_knockout_turn', 'minutes', 'match_players']


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


class MatchCreateSerializer(serializers.ModelSerializer):
    playgroup = serializers.PrimaryKeyRelatedField(
        many=False, queryset=Playgroup.objects.all()
    )
    match_players = MatchPlayerCreateSerializer(many=True, read_only=False)

    class Meta:
        model = Match
        fields = ['id', 'index', 'date', 'number_of_turns', 'first_knockout_turn',
                  'minutes', 'playgroup', 'match_players']
        read_only_fields = ['id', 'index']

    def create(self, validated_data):
        mp = validated_data.pop('match_players')
        index = Match.objects.filter(
            playgroup_id=validated_data['playgroup']).count() + 1

        match = Match.objects.create(index=index, **validated_data)

        for match_player_data in mp:
            commanders = match_player_data.pop('commanders')
            match_player = MatchPlayer.objects.create(
                match=match,
                **match_player_data
            )
            match_player.commanders.set(commanders)

        return match
