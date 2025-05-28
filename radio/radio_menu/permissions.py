from django.db.models.query import Q
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from radio.models import Radio
from radio.models import RadioMenuModel


class IsUserStaff(IsAuthenticated):
    def has_permission(self, request: Request, view: ModelViewSet) -> bool:
        return all([request.user, request.user.is_authenticated])


class IsClientHasRadioMenuPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: ModelViewSet) -> bool:
        is_perm = False
        if view.action in ["create", "update"]:
            radio_id = request.data.get("radio")
            if request.user.roles == "client":
                is_perm = Radio.objects.filter(id=radio_id, user=request.user).exists()
            elif request.user.roles == "admin":
                is_perm = Radio.objects.filter(id=radio_id).exists()
            else:
                is_perm = Radio.objects.filter(
                    Q(user=request.user) | Q(user__created_by=request.user)
                ).exists()
        elif view.action in ["destroy", "partial_update"]:
            url = request.META["PATH_INFO"].split("/")
            menu_id = int(url[len(url) - 2])
            if request.user.roles == "client":
                is_perm = RadioMenuModel.objects.filter(
                    id=menu_id, radio__user=request.user
                ).exists()
            elif request.user.roles == "admin":
                is_perm = RadioMenuModel.objects.filter(id=menu_id).exists()
            else:
                is_perm = RadioMenuModel.objects.filter(
                    Q(radio__user=request.user) | Q(radio__user_created_by=request.user)
                ).exists()
        return is_perm
