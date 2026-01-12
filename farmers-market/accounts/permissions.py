from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsNotSuspended(permissions.BasePermission):
    """
    Permission to check if user is not suspended
    """
    message = 'Your account has been suspended. Contact support for more information.'

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if hasattr(request.user, 'is_suspended') and request.user.is_suspended:
                raise PermissionDenied(
                    f"Your account is suspended. Reason: {request.user.suspension_reason or 'Not specified'}"
                )
        return True
