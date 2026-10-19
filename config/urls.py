from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from .sitemaps import ProjectSitemap, StaticViewSitemap

sitemaps = {"static": StaticViewSitemap, "projects": ProjectSitemap}

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("contact/", include("contact.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots",
    ),
    path("", include("portfolio.urls")),
]
