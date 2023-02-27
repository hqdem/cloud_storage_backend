from rest_framework import permissions


class CheckFileOwnerOnDelete(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ('destroy', 'update', 'partial_update'):
            return request.user == obj.owner
        return True
