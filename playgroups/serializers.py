import uuid

from rest_framework import serializers

from playgroups.models import Commander, Match, MatchPlayer, Player, Playgroup, User


class PlaygroupSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    managers = serializers.PrimaryKeyRelatedField(
        many=True, read_only=False, queryset=User.objects.all()
    )

    class Meta:
        model = Playgroup
        fields = ["id", "name", "owner", "managers"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        # on update
        if self.instance:
            if self.instance.name != attrs["name"]:
                raise serializers.ValidationError(
                    "Playgroup name cannot be changed after creation"
                )
        # on create
        else:
            if self.context["request"].user != attrs["owner"]:
                raise serializers.ValidationError(
                    "Playgroup owner must be current user"
                )

        return attrs


class PlayerSerializer(serializers.ModelSerializer):
    playgroup = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, queryset=Playgroup.objects.all()
    )

    class Meta:
        model = Player
        fields = ["id", "name", "playgroup"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        # ensure the playgroup matches the id in the route
        playgroup_id = uuid.UUID(
            self.context["request"].parser_context["kwargs"]["playgroup_pk"]
        )
        if playgroup_id != attrs["playgroup"].id:
            raise serializers.ValidationError(f"Playgroup id does not match route")
        return attrs


class MatchPlayerSerializer(serializers.ModelSerializer):
    player = serializers.PrimaryKeyRelatedField(
        many=False, queryset=Player.objects.all()
    )
    commanders = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Commander.objects.all()
    )

    class Meta:
        model = MatchPlayer
        fields = ["rank", "turn_position", "player", "commanders"]

    def validate(self, attrs):
        # ensure the playgroup matches the id in the route
        playgroup_id = uuid.UUID(
            self.context["request"].parser_context["kwargs"]["playgroup_pk"]
        )
        if playgroup_id != attrs["player"].playgroup.id:
            raise serializers.ValidationError(
                f"Match player playgroup id does not match route"
            )
        return attrs

    def validate_commanders(self, value):
        if len(value) < 1:
            raise serializers.ValidationError(
                "Match player must have at least one commander"
            )
        return value


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


class CommanderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commander
        fields = ["id", "name", "color_identity", "image", "scryfall_uri"]


class UserSerializer(serializers.ModelSerializer):
    playgroups_owned = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    playgroups_managed = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "username", "playgroups_owned", "playgroups_managed"]
