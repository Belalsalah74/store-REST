from rest_framework import permissions

SAFE_METHODS = permissions.SAFE_METHODS
class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )
