from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ekiladesign.validators import max_size_in_kb


class Publicite(models.Model):
    pub_image = models.FileField(
        _("publicity image"),
        upload_to="uploads/",
        validators=[FileExtensionValidator(allowed_extensions=["png", "jpeg", "jpg"])],
    )
    description = models.TextField(_("description"), blank=True, null=True)
    is_enable = models.BooleanField(_("is enable"), default=True)
    is_created_at = models.DateTimeField(_("is created at"), default=timezone.now)
    is_updated_at = models.DateTimeField(_("is updated at"), auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
    )

    class Meta:
        verbose_name = _("Publicity")
        verbose_name_plural = _("Advertising management")
        ordering = ["-is_created_at"]

    def __str__(self) -> str:
        return f"{self.pub_image.name}"

    def clean(self) -> None:
        if self.pub_image and self.pub_image.size > settings.MAX_PUBLICITE_IMAGE_SIZE:
            message_error = _("Image size must be less than %(size)s KB") % {
                "size": max_size_in_kb
            }
            raise ValidationError(message_error, code="image_size_exceeded")
