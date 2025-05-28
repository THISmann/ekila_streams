from typing import Any
from typing import Dict

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from rest_framework import exceptions
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from .permissions import user_admin_authentication_rule
from ekilauth.authentification.serializers import UserSerializer
from ekilauth.models import EkilaUser
from ekilauth.models import UserRole


class AdminUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EkilaUser
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_confirmed",
            "roles",
        ]
        read_only_fields = ["id"]


class AdminUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = EkilaUser
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_confirmed",
            "roles",
            "password",
            "confirm_password",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        if password != confirm_password:
            raise serializers.ValidationError(
                "Password and confirm password doesn't match"
            )

        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError(e)
        attrs.pop("confirm_password", None)
        return attrs

    def create(self, validated_data: Dict[str, Any]) -> EkilaUser:
        user = self.context["request"].user
        roles = validated_data.get("roles")
        if user and user.roles == UserRole.REVENDEUR and roles != UserRole.CLIENT:
            raise exceptions.PermissionDenied(
                "You are not allowed to create user with role different from client"
            )
        return super().create(validated_data)

    def update(self, instance: EkilaUser, validated_data: Dict[str, Any]) -> EkilaUser:
        user = self.context["request"].user
        new_role = validated_data.get("roles", instance.roles)
        if user and user.roles == UserRole.REVENDEUR and new_role != UserRole.CLIENT:
            raise exceptions.PermissionDenied(
                "You are not allowed to change user role to other than client"
            )
        return super().update(instance, validated_data)

    def save(self, **kwargs):
        super().save(**kwargs)
        if self.instance:
            self.instance.set_password(self.instance.password)
            self.instance.save()


class AdminObtainTokenSerializer(TokenObtainPairSerializer):
    username_field = EkilaUser.EMAIL_FIELD

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        user = authenticate(**authenticate_kwargs)

        if not user_admin_authentication_rule(user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        refresh = self.get_token(user)
        data = {"refresh": str(refresh), "access": str(refresh.access_token)}

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)

        return data
