from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from rest_framework.exceptions import ValidationError


max_size_in_kb = settings.MAX_PUBLICITE_IMAGE_SIZE / 1000


def validate_image_size(value: UploadedFile) -> None:
    if hasattr(value, "size") and value.size > settings.MAX_PUBLICITE_IMAGE_SIZE:
        raise ValidationError(
            f"Image size exceeds the limit {max_size_in_kb} KB", code="invalid"
        )
