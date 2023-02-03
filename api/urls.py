from django.urls import path
from .views import tgBotView, test

urlpatterns = [
    path("sendMessageToken", tgBotView.as_view(), name="sendMessageToken"),
    path("test/", test, name="test"),
]
