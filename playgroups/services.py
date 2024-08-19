import uuid

from django.contrib.auth.models import User

from playgroups.models import Profile


def is_playgroup_admin(profile: Profile, playgroup_id: uuid.UUID):
    return is_playgroup_owner(profile, playgroup_id) or is_playgroup_manager(profile, playgroup_id)


def is_playgroup_owner(profile: Profile, playgroup_id: uuid.UUID):
    playgroups_owned = profile.profile.playgroups_owned.all()
    return playgroup_id in [pg.id for pg in playgroups_owned]
