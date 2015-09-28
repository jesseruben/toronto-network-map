from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # check if the request.user is associated with the obj which is essential an accounts object
        if request.user:
            return obj == request.user
        return False

