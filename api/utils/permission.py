#TODO: Write Custom Permission On Email Verify Access
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    message = ("You are not allowed to update or delete an post that does not belong to you")

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user