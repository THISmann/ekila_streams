from typing import Any
from typing import Dict

from channels.consumer import AsyncConsumer
from django.contrib.auth.models import AnonymousUser
from djangochannelsrestframework.permissions import BasePermission
from rest_framework import permissions
from rest_framework.request import Request

from ekiladesign.models import Publicite


class IsAdminOrClient(permissions.BasePermission):
    def has_permission(self, request: Request, view: Any) -> bool:
        return request.user.roles in ["admin", "client"]

    def has_object_permission(
        self, request: Request, view: Any, obj: Publicite
    ) -> bool:
        return request.user == obj.user


class IsConfirmedWebSocket(BasePermission):
    async def has_permission(
        self, scope: Dict[str, Any], consumer: AsyncConsumer, action: str, **kwargs
    ) -> bool:
        user = scope.get("user")
        if not user or isinstance(user, AnonymousUser):
            return False
        return user and user.is_confirmed
