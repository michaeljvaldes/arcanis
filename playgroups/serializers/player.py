from rest_framework import serializers

from playgroups.models import Player, Playgroup


class PlayerSerializer(serializers.ModelSerializer):
    playgroup = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Player
        fields = ["id", "name", "playgroup"]
        read_only_fields = ["id", "playgroup"]


class PlayerCreateSerializer(serializers.ModelSerializer):
    playgroup = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, queryset=Playgroup.objects.all()
    )

    class Meta:
        model = Player
        fields = ["id", "name", "playgroup"]
        read_only_fields = ["id", "playgroup"]
