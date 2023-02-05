from django.urls import path
from .views import sendFileView

urlpatterns = [
    path("send/", sendFileView.as_view(), name="sendFile"),
]
