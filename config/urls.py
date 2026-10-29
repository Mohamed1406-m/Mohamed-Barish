from django.urls import path
from portfolio import views
urlpatterns = [
    path("", views.home),
    path("api/chat", views.chat),
    path("api/call-token", views.call_token),
]
