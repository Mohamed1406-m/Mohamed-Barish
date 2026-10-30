import os
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from portfolio import views

_ON_VERCEL = os.getenv("VERCEL") == "1"

if not _ON_VERCEL:
    from django.contrib import admin

urlpatterns = [
    *([] if _ON_VERCEL else [path("admin/", admin.site.urls)]),
    path("", views.home),
    path("api/chat", views.chat),
    path("api/call-token", views.call_token),
] + ([] if _ON_VERCEL else static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
