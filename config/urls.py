from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/telegram/sendMessage/', include("sendMessage.urls")),
    path('api/telegram/file/', include("tgFile.urls")),
    path('api/telegram/file/', include("sendFile.urls")),
    path('api/me/', include("api.urls")),
    path('api/', include("djoser.urls")),
    path('api/', include("djoser.urls.authtoken")),
    re_path(r"^static/(.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    re_path(r"^media/(.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
