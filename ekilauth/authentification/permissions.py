from rest_framework import permissions

from ekilauth.models import EkilaUser


def user_authentication_rule(user: EkilaUser) -> bool:
    return user is not None and user.is_confirmed


class IsConfirmedUser(permissions.BasePermission):
    message = "User is not confirmed."

    def has_permission(self, request, view):
        user = request.user
        return user_authentication_rule(user)
