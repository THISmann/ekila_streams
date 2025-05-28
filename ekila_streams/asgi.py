"""
ASGI config for ekila_streams project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import os

from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ekila_streams.settings")

django_asgi_app = get_asgi_application()

from ekiladesign.consumers import PublicityConsumer
from radio.consumers import RadioConsumer
from channels_auth_token_middlewares.middleware import (
    QueryStringSimpleJWTAuthTokenMiddleware,
)

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": QueryStringSimpleJWTAuthTokenMiddleware(
            URLRouter(
                [
                    path("ws/publicity/", PublicityConsumer.as_asgi()),
                    path("ws/radio/", RadioConsumer.as_asgi()),
                ]
            )
        ),
    }
)
