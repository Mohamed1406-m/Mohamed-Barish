from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from portfolio import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home),
    path("api/chat", views.chat),
    path("api/call-token", views.call_token),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
