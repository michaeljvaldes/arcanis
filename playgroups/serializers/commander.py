from rest_framework import serializers

from playgroups.models import Commander


class CommanderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commander
        fields = ['id', 'name', 'color_identities', 'image', 'scryfall_uri']
