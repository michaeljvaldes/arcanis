import uuid

from rest_framework import serializers

from playgroups.models import Commander, MatchPlayer, Player


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
