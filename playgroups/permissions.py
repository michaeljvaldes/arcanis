import uuid

from rest_framework import permissions

from playgroups.services import is_playgroup_admin, is_playgroup_owner


class PlaygroupPermission(permissions.BasePermission):
    """
    Custom permission to limit unsafe actions on playgroups. Any
    authenticated user may create a playgroup, but changing an
    existing playgroup requires further permissions. The playgroup
    is obtained from the url route and compared with the permissions of
    the user.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return is_playgroup_owner(request.user, obj.id)
        return False


class PlaygroupChildPermission(permissions.BasePermission):
    """
    Custom permission to limit unsafe actions on a playgroup child
    model to the owner or a manager of that playgroup. The playgroup
    is obtained from the url route and compared with the permissions of
    the user.
    """

    def has_permission(self, request, view):
        return self.is_playgroup_admin_or_read_only(request, view)

    def has_object_permission(self, request, view, obj):
        return self.is_playgroup_admin_or_read_only(request, view)

    def is_playgroup_admin_or_read_only(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        playgroup_id = self.get_playgroup_id(view)
        if request.user.is_authenticated and playgroup_id:
            return is_playgroup_admin(
                request.user, playgroup_id=uuid.UUID(playgroup_id)
            )
        return False

    def get_playgroup_id(self, view):
        if "playgroup_pk" in view.kwargs:
            return view.kwargs["playgroup_pk"]
        return None
