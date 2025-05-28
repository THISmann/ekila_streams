from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from ekilauth.user.models import EkilaUser


class IsAdminOrVendor(permissions.BasePermission):
    def has_permission(self, request: Request, view: ModelViewSet) -> bool:
        return request.user.roles in ["admin", "revendeur"]

    def has_object_permission(
        self, request: Request, view: ModelViewSet, obj: EkilaUser
    ) -> bool:
        perm_for_dealer = obj.created_by and (obj.created_by.id == request.user.id)
        perm_for_admin = request.user.roles == "admin" and (
            obj.roles != "admin" or view.action == "retrieve"
        )
        return perm_for_dealer or perm_for_admin


def user_admin_authentication_rule(user: EkilaUser) -> bool:
    return (
        user is not None and user.is_confirmed and user.roles in ["admin", "revendeur"]
    )
