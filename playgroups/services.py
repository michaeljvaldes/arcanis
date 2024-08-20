import uuid

from django.contrib.auth.models import User

from playgroups.models import User


def is_playgroup_admin(user: User, playgroup_id: uuid.UUID):
    return is_playgroup_owner(user, playgroup_id) or is_playgroup_manager(
        user, playgroup_id
    )


def is_playgroup_owner(user: User, playgroup_id: uuid.UUID):
    playgroups_owned = user.playgroups_owned.all()
    return playgroup_id in [pg.id for pg in playgroups_owned]


def is_playgroup_manager(user: User, playgroup_id: uuid.UUID):
    playgroups_managed = user.playgroups_managed.all()
    return playgroup_id in [pg.id for pg in playgroups_managed]
