from django.db.models import QuerySet
from django.db.models.query import Q
from rest_framework.viewsets import ModelViewSet

from radio.models import RadioMenuModel
from radio.radio_menu.permissions import IsClientHasRadioMenuPermission
from radio.radio_menu.permissions import IsUserStaff
from radio.serializers import RadioMenuSerializer


class RadioMenuViewSet(ModelViewSet):
    queryset = RadioMenuModel.objects.all()
    serializer_class = RadioMenuSerializer
    permission_classes = (IsUserStaff,)

    def get_queryset(self) -> QuerySet:
        if self.request.user.roles == "admin":
            return self.queryset
        elif self.request.user.roles == "client":
            return self.queryset.filter(radio__user=self.request.user)
        else:
            return self.queryset.filter(
                Q(radio__user=self.request.user)
                | Q(radio__user_created_by=self.request.user)
            )

    def get_permissions(self):
        if self.action in ["create", "update", "destroy", "partial_update"]:
            self.permission_classes = [IsClientHasRadioMenuPermission]
        return super().get_permissions()
