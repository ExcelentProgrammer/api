from django.urls import path
from .views import tgBotView, test

urlpatterns = [
    path("createToken/", tgBotView.as_view(), name="createToken"),
    path("test/", test, name="test"),
]
