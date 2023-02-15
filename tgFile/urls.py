from django.urls import path
from .views import DownloadAPI

urlpatterns = [
    path("download/",DownloadAPI.as_view(),name="download")
]