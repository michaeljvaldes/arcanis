from rest_framework import serializers

from playgroups.models import Playgroup, User


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
