from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from radio.models import Radio


class IsOwnerOrVendorOrAdmin(IsAuthenticated):
    def has_object_permission(
        self, request: Request, view: ModelViewSet, obj: Radio
    ) -> bool:
        permission_for_admin = request.user.roles == "admin"
        permission_for_client = obj.user == request.user
        permission_for_vendor = (
            permission_for_client or obj.user.created_by == request.user
        )
        return permission_for_admin or permission_for_vendor or permission_for_client

    def has_permission(self, request: Request, view: ModelViewSet) -> bool:
        return all([request.user, request.user.is_authenticated])


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request: Request, view: ModelViewSet) -> bool:
        return request.user.is_authenticated and request.user.roles in ["admin"]
