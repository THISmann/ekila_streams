import mimetypes
import os

mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("text/js", ".js", True)

DEBUG = True
STATIC_ROOT = os.getenv("DJANGO_STATIC_ROOT")
STATIC_URL = "/var/www/static/"

ALLOWED_HOSTS = ["*"]

# cors configuration
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    os.getenv("FRONT_HOST", "http://localhost:8030"),
]

# Media files (Images)
MEDIA_ROOT = os.getenv("DJANGO_MEDIA_ROOT", "/var/wwww/media")
MEDIA_URL = "/media/"

# Postgre DB conf
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.getenv("POSTGRES_HOST", "db"),
        "NAME": "ekila_db",
        "USER": "postgres",
        "PASSWORD": "8Fny?aXEFkh9ePA3",
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

FRONT_END_URL = os.getenv("FRONTEND_URL")

ASGI_APPLICATION = "ekila_streams.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}
