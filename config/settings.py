import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-key")
DEBUG = os.getenv("DEBUG", "1") == "1"
ALLOWED_HOSTS = [".vercel.app", "localhost", "127.0.0.1", "mdbarish.in", "www.mdbarish.in"]

# True when a real DB is available (Neon on Vercel, or local SQLite)
_HAS_DB = bool(os.getenv("DATABASE_URL")) or not (os.getenv("VERCEL") == "1")

INSTALLED_APPS = [
    *([
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
    ] if _HAS_DB else []),
    "django.contrib.staticfiles",
    "storages",
    "portfolio",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    *([
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ] if _HAS_DB else []),
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]

ROOT_URLCONF = "config.urls"

_ctx = ["django.template.context_processors.request"]
if _HAS_DB:
    _ctx += [
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": _ctx},
}]

WSGI_APPLICATION = "config.wsgi.application"

# Database — Neon PostgreSQL when DATABASE_URL is set, else local SQLite
import dj_database_url
_db_url = os.getenv("DATABASE_URL")
if _db_url:
    DATABASES = {"default": dj_database_url.parse(_db_url, conn_max_age=600, ssl_require=True)}
elif not (os.getenv("VERCEL") == "1"):
    DATABASES = {"default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }}
else:
    DATABASES = {}

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "public" / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
WHITENOISE_AUTOREFRESH = True  # pick up files written to /tmp/staticfiles at runtime

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Neon S3-compatible storage for media files (profile photos, project images)
_S3_ENDPOINT = os.getenv("AWS_ENDPOINT_URL_S3")
if _S3_ENDPOINT:
    STORAGES = {
        "default": {"BACKEND": "portfolio.storage.ProxiedS3Storage"},
        "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
    }
    AWS_ENDPOINT_URL_S3 = _S3_ENDPOINT
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION_NAME = os.getenv("AWS_REGION", "ap-southeast-1")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", "neondb")
    AWS_S3_FILE_OVERWRITE = False
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_ADDRESSING_STYLE = "path"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    MEDIA_URL = "/media/"

CSRF_TRUSTED_ORIGINS = ["https://www.mdbarish.in", "https://mdbarish.in"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
