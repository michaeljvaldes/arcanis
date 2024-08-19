import uuid

from rest_framework import permissions

from playgroups.services import is_playgroup_admin


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user


class IsPlaygroupAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to limit unsafe actions on a playgroup and its 
    children to the owner or a manager of that playgroup. The playgroup
    is obtained from the url route and the permissions for that playgroup
    are obtained from the user profile.
    """

    def is_playgroup_admin_or_read_only(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        if request.user.is_authenticated and request.user.profile is not None:
            return is_playgroup_admin(request.user.profile, playgroup_id=uuid.UUID(view.kwargs['playgroup_pk']))
        return False

    def has_permission(self, request, view):
        return self.is_playgroup_admin_or_read_only(request, view)

    def has_object_permission(self, request, view, obj):
        return self.is_playgroup_admin_or_read_only(request, view)
