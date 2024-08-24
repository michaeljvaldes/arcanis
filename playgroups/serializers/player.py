import uuid

from rest_framework import serializers

from playgroups.models import Player, Playgroup


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
