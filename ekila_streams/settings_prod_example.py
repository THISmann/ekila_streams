import mimetypes
import os

mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("text/js", ".js", True)

DEBUG = False

STATIC_ROOT = os.getenv("DJANGO_STATIC_ROOT", "/var/www/static")
STATIC_URL = "/static/"

ALLOWED_HOSTS = [
    "admin.radiowebapp.com",
    "https://admin.radiowebapp.com",
    "178.32.43.101",
    "https://178.32.43.101:443",
    "0.0.0.0",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "/var/www/radiowebapp/ekila_streams/ekilauth/authentification/templates/"
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# cors configuration
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    os.getenv("FRONT_HOST", "https://radiowebapp.com"),
]

SECURE_SSL_REDIRECT = True

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Media files (Images)
MEDIA_ROOT = os.getenv("DJANGO_MEDIA_ROOT", "/var/www/media")
MEDIA_URL = "/media/"

# Postgre DB conf
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.getenv("POSTGRES_HOST", "127.0.0.1"),
        "NAME": "ekila_db",
        "USER": "postgres",
        "PASSWORD": os.getenv("PGPASS", "h37ZXHuA"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

CSRF_TRUSTED_ORIGINS = ["https://admin.radiowebapp.com"]

FRONT_END_URL = os.getenv("FRONTEND_URL", "https://radiowebapp.com/#/reset/password")
