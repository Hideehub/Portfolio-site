from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from portfolio.models import Project


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 1.0

    def items(self):
        return ["portfolio:home"]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Project.objects.all()
