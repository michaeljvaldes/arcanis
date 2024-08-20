from rest_framework import serializers

from playgroups.models import Playgroup


class PlaygroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playgroup
        fields = ['id', 'name']
        read_only_fields = ['id']
