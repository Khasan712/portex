from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static
from app.views import home, install_sh, ProxyView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('install/', install_sh),
    re_path(r'^(?P<path>.*)$', ProxyView.as_view(), name='proxy')
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
) + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)
