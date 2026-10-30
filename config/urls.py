import os
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from portfolio import views

_HAS_DB = bool(os.getenv("DATABASE_URL")) or not (os.getenv("VERCEL") == "1")

if _HAS_DB:
    from django.contrib import admin

urlpatterns = [
    *([path("admin/", admin.site.urls)] if _HAS_DB else []),
    path("", views.home),
    path("api/chat", views.chat),
    path("api/call-token", views.call_token),
    path("api/set-bucket-public", views.set_bucket_public),
] + (static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) if _HAS_DB else [])
