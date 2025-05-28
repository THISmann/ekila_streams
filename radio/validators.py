import re
import string

from django.core.exceptions import ValidationError


def validate_url_flux_radio(pattern, url):
    if re.match(pattern, url) is None:
        raise ValidationError("URL du flux non valide, regarde la documentation :)")


def validate_url_server_radio(value):
    regex = r"^(http:\/\/|https:\/\/)[a-zA-Z0-9.-]+\.[a-z]{2,5}(:[0-9]{1,5})?$"
    if re.match(regex, value) is None:
        raise ValidationError(
            "URl format must be http:///IP_OR_HOSTNAME:PORT \
            or https:///IP_OR_HOSTNAME:PORT"
        )


def validate_radio_name(value: str):
    if " " in value or "-" in value or (value.isascii() is False):
        raise ValidationError(
            "Pas de tiret ni de charactère special, nom Publish Name requis comme\
            dans le panel radio"
        )
    for v in value:
        if v in string.punctuation:
            raise ValidationError(
                "Pas de tiret ni de charactère special, nom Publish Name requis comme\
            dans le panel radio"
            )
