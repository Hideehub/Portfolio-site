from django.shortcuts import get_object_or_404, render

from contact.forms import ContactForm

from .models import Project

# Shown in the About section. Edit freely.
SKILLS = [
    ("Backend", ["Python", "Django", "PostgreSQL", "Celery", "Redis", "pytest"]),
    ("Frontend", ["HTML", "CSS", "JavaScript", "Django templates", "HTMX", "Tailwind CSS"]),
    ("Tools", ["Git & GitHub", "GitHub Actions", "Docker", "Render", "Neon", "Cloudflare R2"]),
]


def render_home(request, contact_form=None, status=200):
    context = {
        "projects": Project.objects.filter(is_featured=True),
        "skills": SKILLS,
        "contact_form": contact_form or ContactForm(),
    }
    return render(request, "portfolio/home.html", context, status=status)


def home(request):
    return render_home(request)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, "portfolio/project_detail.html", {"project": project})
