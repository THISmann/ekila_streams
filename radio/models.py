from typing import Iterable

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from ekilauth.user.models import EkilaUser


class TypeRadio(models.TextChoices):
    SHOUTCAST = "shoutcast", "Shoutcast"
    ICECAST = "icecast", "Icecast"
    EVERESTCAST = "everestcast", "EverestCast"
    CENTOVACAST = "centovacast", "CentovaCast"
    MEDIACP = "rcast", "Rcast"
    AZURACAST = "azuracast", "AzuraCast"
    EVERESTPANEL = "everestpanel", "EverestPanel"
    RADIOKING = "radioking", "RadioKing"


class Radio(models.Model):
    name = models.CharField(_("name"), max_length=255)
    url_flux_radio = models.URLField(_("url flux radio"), null=True, blank=True)
    url_server_radio = models.URLField(_("url server radio"), blank=True)
    url_api_radio_history = models.URLField(
        _("url api radio history"), null=True, blank=True
    )
    url_api_radio_current_song = models.URLField(
        _("url api radio current song"), null=True, blank=True
    )
    sid = models.IntegerField(_("sid"), null=True, blank=True, default=1)
    radio_account_port = models.IntegerField(
        _("radio account port"), null=True, blank=True
    )
    station_id = models.IntegerField(_("station id"), null=True, blank=True)
    url_pannel_connexion = models.URLField(
        _("url pannel connexion"), null=True, blank=True
    )
    username_radio_account = models.CharField(
        _("username radio account"), max_length=255, blank=True, null=True
    )
    id_radioking = models.IntegerField(_("id radioking"), null=True, blank=True)
    url_cover_default = models.URLField(_("url cover default"))
    url_site = models.URLField(_("url site"))
    server_type = models.CharField(
        _("server type"),
        max_length=50,
        choices=TypeRadio.choices,
        default=TypeRadio.SHOUTCAST,
    )
    user = models.ForeignKey(
        EkilaUser,
        on_delete=models.CASCADE,
        related_name="user_radio",
        verbose_name=_("user"),
    )
    radio_image_icon = models.FileField(
        _("radio image icon"),
        upload_to="uploads/",
        validators=[FileExtensionValidator(allowed_extensions=["png", "jpeg", "jpg"])],
        blank=True,
    )
    is_active = models.BooleanField(_("is active"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Radio")
        verbose_name_plural = _("Radio management")
        indexes = [models.Index(fields=["user"], name="radio_by_user")]
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_radio_name")
        ]

    def __str__(self):
        return self.name


class RadioMenuModel(models.Model):
    title = models.CharField(_("title"), max_length=255)
    link = models.URLField(_("link"))
    radio = models.ForeignKey(
        Radio,
        on_delete=models.CASCADE,
        related_name="radio_menu",
        verbose_name=_("radio"),
    )

    class Meta:
        verbose_name = _("radio menu")
        verbose_name_plural = _("radio menus")

    def __str__(self) -> str:
        return self.title


# class RadioMetadaDataTemporary(models.Model):
#     radio_id = models.IntegerField()
#     title = models.CharField(max_length=120, blank=True, null=True)
#     album_title = models.CharField(max_length=120, blank=True, null=True)
#     cover = models.CharField(max_length=120, blank=True, null=True)
#     artist_name = models.CharField(max_length=120, blank=True, null=True)
#     created_at = models.DateTimeField(_("created at"), auto_now_add=True)

#     class Meta:
#         ordering = ["created_at"]
