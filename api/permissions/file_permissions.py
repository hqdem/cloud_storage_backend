from rest_framework import permissions


class CheckFileOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if view.action in ['add_shared_user', 'delete_shared_user']:
            return user == obj.owner
        if user == obj.owner or user in obj.shared_users.all():
            return True

        parent_dir = obj.directory
        while parent_dir:
            if user in parent_dir.shared_users.all():
                return True
            parent_dir = parent_dir.parent_dir
        return False
