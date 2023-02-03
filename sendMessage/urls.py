from django.urls import path
from .views import sendMessage

urlpatterns = [
    path("", sendMessage.as_view(), name="sendMessage"),
]
