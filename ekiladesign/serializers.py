from django.conf import settings
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ekiladesign.models import Publicite
from ekiladesign.validators import max_size_in_kb
from ekiladesign.validators import validate_image_size


image_help_text = f"Image size should be less than {max_size_in_kb} KB"


class TimeStampSerializer(ModelSerializer):
    is_created_at = serializers.DateTimeField(
        read_only=True, format=settings.DATETIME_FORMAT
    )
    is_updated_at = serializers.DateTimeField(
        read_only=True, format=settings.DATETIME_FORMAT
    )


class PubliciteCreateSerializer(TimeStampSerializer):
    pub_image = serializers.FileField(
        required=True,
        help_text=image_help_text,
        validators=[validate_image_size],
    )

    class Meta:
        model = Publicite
        exclude = ["user"]
        read_only_fields = [
            "id",
            "is_enable",
            "is_created_at",
            "is_updated_at",
        ]


class PubliciteDetailSerializer(TimeStampSerializer):
    class Meta:
        model = Publicite
        fields = [
            "id",
            "pub_image",
            "description",
            "is_enable",
            "is_created_at",
            "is_updated_at",
        ]


class PubliciteUpdateSerializer(TimeStampSerializer):
    pub_image = serializers.FileField(
        required=False,
        help_text=image_help_text,
        validators=[validate_image_size],
    )
    description = serializers.CharField(required=False)

    class Meta:
        model = Publicite
        fields = ["id", "pub_image", "description", "is_enable", "is_updated_at"]


class WebSocketPublicitySerializer(serializers.Serializer):
    action = serializers.CharField()
    publicity = PubliciteDetailSerializer()
