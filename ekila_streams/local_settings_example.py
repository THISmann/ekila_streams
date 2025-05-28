from pathlib import Path

SECRET_KEY = "****************************************"
BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
