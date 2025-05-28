import ast

from django.db.models import QuerySet
from django.db.models.query import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from ekilauth.authentification.permissions import IsConfirmedUser
from radio.domain.metadata import RadioMedata
from radio.models import Radio
from radio.permissions import IsAdmin
from radio.permissions import IsOwnerOrVendorOrAdmin
from radio.serializers import AdminRadioSerializer
from radio.serializers import MedataRadioSerializer
from radio.serializers import RadioCreateOrUpdateSerializer
from radio.serializers import RadioDetailSerializer
from radio.serializers import RadioSerializer


class RadioViewSet(ModelViewSet):
    serializer_class = RadioSerializer
    permission_classes = (IsOwnerOrVendorOrAdmin, IsConfirmedUser)
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer: Serializer) -> None:
        user = self.request.user
        serializer.save(user=user)

    def get_permissions(self):
        if self.action == "admin":
            self.permission_classes = [IsAdmin]
        elif self.action in ("get_by_name", "get_stream_result"):
            self.permission_classes = []
        return super().get_permissions()

    def get_serializer_class(self) -> Serializer:
        if self.action in ("list", "retrieve"):
            return RadioDetailSerializer
        elif self.action in ("create", "update"):
            return RadioCreateOrUpdateSerializer
        elif self.action == "admin":
            return AdminRadioSerializer
        elif self.action == "get_stream_result":
            return MedataRadioSerializer
        return RadioSerializer

    @action(
        detail=False,
        methods=["get"],
        url_path="name/(?P<name>.+)",
        lookup_field="name",
    )
    def get_by_name(self, request: Request, name: str) -> Response:
        radio = self.get_object()
        serializer = self.get_serializer(radio)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self) -> QuerySet:
        if not self.request.user.is_authenticated:
            return Radio.objects.all()
        else:
            if self.request.user.roles == "admin":
                return Radio.objects.all()
            elif self.request.user.roles == "client":
                return Radio.objects.filter(user=self.request.user)
            else:
                return Radio.objects.filter(
                    Q(user=self.request.user) | Q(user__created_by=self.request.user)
                )

    @action(detail=True, methods=["get"])
    def activate(self, request: Request, **kwargs) -> Response:
        radio = self.get_object()
        radio.is_active = True
        radio.save()
        return Response(
            {"message": "The radio has been successfully activated"},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get"])
    def deactivate(self, request: Request, **kwargs) -> Response:
        radio = self.get_object()
        radio.is_active = False
        radio.save()
        return Response(
            {"message": "The radio has been successfully deactivated"},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"])
    def admin(self, request: Request, **kwargs) -> Response:
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "The radio has been successfully created"},
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["get"],
        url_path="metadata/(?P<name>.+)",
        lookup_field="name",
    )
    def get_stream_result(self, request: Request, **kwargs) -> Response:
        radio = self.get_object()
        metadata = RadioMedata.make_requests(radio=radio)
        if isinstance(metadata, RadioMedata):
            data = ast.literal_eval(RadioMedata.from_cls_to_dict(metadata))
            serializer = self.get_serializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(metadata, status=status.HTTP_200_OK)
