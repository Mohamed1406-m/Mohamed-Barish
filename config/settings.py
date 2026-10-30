import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-key")
DEBUG = os.getenv("DEBUG", "1") == "1"
ALLOWED_HOSTS = [".vercel.app", "localhost", "127.0.0.1", "mdbarish.in", "www.mdbarish.in"]

_ON_VERCEL = os.getenv("VERCEL") == "1"
INSTALLED_APPS = [
    *([] if _ON_VERCEL else [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
    ]),
    "django.contrib.staticfiles",
    "portfolio",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    *([] if _ON_VERCEL else [
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ]),
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]

ROOT_URLCONF = "config.urls"

_vercel_ctx = ["django.template.context_processors.request"]
_local_ctx = _vercel_ctx + [
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
]
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": _vercel_ctx if _ON_VERCEL else _local_ctx},
}]

WSGI_APPLICATION = "config.wsgi.application"

# SQLite for local dev; Vercel filesystem is read-only so disable DB there
DATABASES = {} if _ON_VERCEL else {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "public" / "static"]
# Use hashed storage locally; on Vercel public/ is served directly so use simple storage
STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedStaticFilesStorage" if _ON_VERCEL
    else "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

CSRF_TRUSTED_ORIGINS = ["https://www.mdbarish.in", "https://mdbarish.in"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
