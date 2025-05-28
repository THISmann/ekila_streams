from typing import Type

from django.db.models import QuerySet
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import EkilaUser
from .permissions import IsAdminOrVendor
from .serializers import AdminObtainTokenSerializer
from .serializers import AdminUserDetailSerializer
from .serializers import AdminUserSerializer
from ekilauth.authentification.permissions import IsConfirmedUser


class AdminObtainTokenView(TokenObtainPairView):
    serializer_class = AdminObtainTokenSerializer


class AdminUserViewSetViewSet(viewsets.ModelViewSet):
    queryset = EkilaUser.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (IsAuthenticated, IsConfirmedUser, IsAdminOrVendor)

    def perform_create(self, serializer: Serializer) -> None:
        user = self.request.user
        serializer.save(created_by=user)

    def get_queryset(self) -> QuerySet:
        if self.request.user.roles == "admin":
            return self.queryset
        return self.queryset.filter(created_by=self.request.user)

    def get_serializer_class(
        self,
    ) -> Type[AdminUserDetailSerializer | AdminUserSerializer]:
        if self.action in ["retrieve", "update", "partial_update"]:
            return AdminUserDetailSerializer
        return self.serializer_class

    @action(detail=True, methods=["get"])
    def activate(self, request: Request, **kwargs) -> Response:
        user = self.get_object()
        user.is_confirmed = True
        user.save()
        return Response(
            {"message": "The user has been successfully activated"},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get"])
    def deactivate(self, request: Request, **kwargs) -> Response:
        user = self.get_object()
        user.is_confirmed = False
        user.save()
        return Response(
            {"message": "The user has been successfully deactivated"},
            status=status.HTTP_200_OK,
        )
