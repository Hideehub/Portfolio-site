import pytest
from django.urls import reverse

from portfolio.models import Project

pytestmark = pytest.mark.django_db


def test_home_lists_featured_projects(client):
    Project.objects.create(
        title="Hidden",
        slug="hidden",
        summary="Not featured.",
        description="",
        tech_stack="Django",
        image_path="img/projects/talentflow.webp",
        is_featured=False,
    )
    response = client.get(reverse("portfolio:home"))
    assert response.status_code == 200
    content = response.content.decode()
    assert "Booking Platform" in content
    assert "TalentFlow" in content
    assert "Hidden" not in content
    assert content.count("<h1") == 1


def test_project_detail(client):
    response = client.get(reverse("portfolio:project_detail", args=["booking-platform"]))
    assert response.status_code == 200
    content = response.content.decode()
    assert "Paystack" in content
    assert "https://booking-platform-2agt.onrender.com" in content
    assert content.count("<h1") == 1


def test_project_detail_hides_blank_links(client):
    Project.objects.filter(slug="talentflow").update(live_url="", repo_url="")
    response = client.get(reverse("portfolio:project_detail", args=["talentflow"]))
    assert response.status_code == 200
    content = response.content.decode()
    assert "View live site" not in content
    assert "View code" not in content


def test_project_detail_404_for_unknown_slug(client):
    response = client.get(reverse("portfolio:project_detail", args=["does-not-exist"]))
    assert response.status_code == 404
    assert "Page not found" in response.content.decode()


def test_sitemap_lists_projects(client):
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    assert b"/projects/talentflow/" in response.content


def test_robots_txt(client):
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert response["Content-Type"].startswith("text/plain")
    assert b"Sitemap: http://testserver/sitemap.xml" in response.content
