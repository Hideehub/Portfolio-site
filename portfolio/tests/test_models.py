import pytest
from django.db import IntegrityError, transaction

from portfolio.models import Project


def make_project(**kwargs):
    defaults = {
        "title": "Example",
        "slug": "example",
        "summary": "An example project.",
        "description": "Longer description.",
        "tech_stack": "Django, PostgreSQL",
        "image_path": "img/projects/example.webp",
    }
    defaults.update(kwargs)
    return Project.objects.create(**defaults)


@pytest.mark.django_db
class TestProject:
    def test_seed_migration_creates_featured_projects_in_order(self):
        projects = list(Project.objects.filter(is_featured=True))
        assert [p.slug for p in projects] == ["booking-platform", "talentflow"]
        assert projects[1].live_url == "https://talentflow-ixq5.onrender.com"

    def test_ordered_by_order_field(self):
        Project.objects.all().delete()
        make_project(title="Third", slug="third", order=30)
        make_project(title="First", slug="first", order=10)
        make_project(title="Second", slug="second", order=20)
        assert [p.slug for p in Project.objects.all()] == ["first", "second", "third"]

    def test_slug_is_unique(self):
        make_project(slug="same")
        with pytest.raises(IntegrityError), transaction.atomic():
            make_project(title="Other", slug="same")

    def test_absolute_url_uses_slug(self):
        project = make_project(slug="my-project")
        assert project.get_absolute_url() == "/projects/my-project/"

    def test_tech_list_strips_whitespace_and_blanks(self):
        project = make_project(tech_stack=" Django ,PostgreSQL,, HTMX , ")
        assert project.tech_list() == ["Django", "PostgreSQL", "HTMX"]

    def test_tech_list_empty(self):
        assert make_project(tech_stack="").tech_list() == []
