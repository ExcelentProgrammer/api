from django.urls import path
from .views import getTokenView, TestPage, getConvertFormats

urlpatterns = [
    path("getToken/", getTokenView.as_view()),
    path("getConvertFormats/", getConvertFormats.as_view()),
    path("test/", TestPage.as_view()),
]
