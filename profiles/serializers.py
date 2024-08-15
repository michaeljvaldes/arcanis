from rest_framework import serializers

from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'favorite_commander',
                  'moxfield_id', 'archidekt_id', 'toski_id']
