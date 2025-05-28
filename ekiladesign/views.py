from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer

from .models import Publicite
from .permissions import IsAdminOrClient
from .serializers import PubliciteCreateSerializer
from .serializers import PubliciteDetailSerializer
from .serializers import PubliciteUpdateSerializer
from ekilauth.authentification.permissions import IsConfirmedUser


@extend_schema_view(
    create=extend_schema(
        description="Create a new advertisement. Only admin and client can create an advertisement",
        summary="Create a new advertisement",
    ),
    update=extend_schema(
        description="Update an advertisement",
        summary="Update an advertisement",
    ),
    partial_update=extend_schema(
        description="Update an advertisement",
        summary="partially modify an advertisement",
    ),
    destroy=extend_schema(
        description="Delete an advertisement",
        summary="Delete an ad by the user who created it",
    ),
    list=extend_schema(
        description="list all activated advertisements of a user",
        summary="List all advertisements",
    ),
    retrieve=extend_schema(
        description="Retrieve an advertisement by its id",
        summary="Retrieve an advertisement",
    ),
)
class PubliciteViewSet(viewsets.ModelViewSet):
    serializer_class = PubliciteDetailSerializer
    permission_classes = (
        IsAuthenticated,
        IsConfirmedUser,
        IsAdminOrClient,
    )
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_class(self) -> Serializer:
        action = self.action
        if action == "create":
            return PubliciteCreateSerializer
        elif action == "update" or action == "partial_update":
            return PubliciteUpdateSerializer
        else:
            return self.serializer_class

    def get_queryset(self) -> QuerySet:
        user = self.request.user
        queryset = Publicite.objects.filter(user=user).order_by("-is_created_at")
        if self.action == "list":
            return queryset.filter(is_enable=True)
        return queryset

    def perform_create(self, serializer: Serializer) -> None:
        print(self.request.user)
        serializer.save(user=self.request.user)
