"""
URL configuration for Suite de Soporte Innovex.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),

    # API apps
    path("api/", include("apps.certificados.urls")),
    path("api/", include("apps.revisor.urls")),
    path("api/", include("apps.portal.urls")),

    # Direct static aliases
    path("logo.png", RedirectView.as_view(url="/static/assets/innovex-logo.png", permanent=False)),
    path("favicon.ico", RedirectView.as_view(url="/static/assets/innovex-logo.png", permanent=False)),

    # Frontend – serve index.html at root
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
