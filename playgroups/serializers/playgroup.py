from rest_framework import serializers

from playgroups.models import Playgroup, User


class PlaygroupSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    managers = serializers.PrimaryKeyRelatedField(
        many=True, read_only=False, queryset=User.objects.all()
    )

    class Meta:
        model = Playgroup
        fields = ["id", "name", "owner", "managers"]
        read_only_fields = ["id"]


class PlaygroupUpdateSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, queryset=User.objects.all()
    )
    managers = serializers.PrimaryKeyRelatedField(
        many=True, read_only=False, queryset=User.objects.all()
    )

    class Meta:
        model = Playgroup
        fields = ["id", "name", "owner", "managers"]
        read_only_fields = ["id", "name"]


class PlaygroupCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    managers = serializers.PrimaryKeyRelatedField(
        many=True, read_only=False, queryset=User.objects.all()
    )

    class Meta:
        model = Playgroup
        fields = ["id", "name", "owner", "managers"]
        read_only_fields = ["id", "owner"]
