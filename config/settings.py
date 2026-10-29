import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-key")
DEBUG = os.getenv("DEBUG", "1") == "1"
ALLOWED_HOSTS = [".vercel.app", "localhost", "127.0.0.1","mdbarish.in"]
INSTALLED_APPS = ["django.contrib.staticfiles", "portfolio"]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware", "django.middleware.csrf.CsrfViewMiddleware"]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "APP_DIRS": True,
              "OPTIONS": {"context_processors": []}}]
WSGI_APPLICATION = "config.wsgi.application"
DATABASES = {}
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "public" / "static"]  # on Vercel, /public is served as static
CSRF_TRUSTED_ORIGINS = ["https://*.vercel.app"]
