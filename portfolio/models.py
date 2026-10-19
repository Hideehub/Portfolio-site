from django.db import models
from django.urls import reverse


class Project(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    summary = models.CharField(max_length=200, help_text="One sentence, shown on the project card.")
    description = models.TextField()
    tech_stack = models.CharField(
        max_length=300, help_text="Comma-separated, e.g. Django, PostgreSQL, HTMX"
    )
    image_path = models.CharField(
        max_length=200,
        help_text="Path inside static/, e.g. img/projects/booking-platform.webp",
    )
    live_url = models.URLField(blank=True)
    repo_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("portfolio:project_detail", kwargs={"slug": self.slug})

    def tech_list(self):
        """Return tech_stack as a list, ignoring blanks and extra whitespace."""
        return [item.strip() for item in self.tech_stack.split(",") if item.strip()]
