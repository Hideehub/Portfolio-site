from django.db import migrations

PROJECTS = [
    {
        "slug": "booking-platform",
        "title": "Booking Platform",
        "summary": (
            "Online booking with deposits for clinics, salons and consultants, "
            "with no double-bookings."
        ),
        "description": (
            "Customers choose a service, staff member and time slot, then secure it with a "
            "deposit via Paystack. Owners manage services, staff, working hours and bookings "
            "from their own dashboard. Double-bookings are blocked by a Postgres constraint, "
            "so even simultaneous requests can't claim the same slot. Celery workers release "
            "unpaid holds and send confirmation and reminder emails. Each business's data is "
            "fully isolated and covered by tests."
        ),
        "tech_stack": (
            "Django, PostgreSQL, Celery, Redis, HTMX, Tailwind CSS, Paystack, Docker"
        ),
        "image_path": "img/projects/booking-platform.webp",
        "live_url": "https://booking-platform-2agt.onrender.com",
        "repo_url": "",
        "is_featured": True,
        "order": 1,
    },
    {
        "slug": "talentflow",
        "title": "TalentFlow",
        "summary": (
            "A private hiring workspace where recruiting teams track candidates "
            "from application to offer."
        ),
        "description": (
            "An applicant tracking system where each company gets its own isolated workspace "
            "for jobs, candidates, interviews and feedback. Recruiters, hiring managers and HR "
            "admins each see only what their role allows. Interviewers can't see colleagues' "
            "feedback until they submit their own, and every status change is logged. "
            "Candidates can be bulk-imported from Excel with row-by-row validation, and "
            "resumes are stored privately behind permission checks."
        ),
        "tech_stack": (
            "Django 6, PostgreSQL, Cloudflare R2, pytest, GitHub Actions, Render"
        ),
        "image_path": "img/projects/talentflow.webp",
        "live_url": "https://talentflow-ixq5.onrender.com",
        "repo_url": "",
        "is_featured": True,
        "order": 2,
    },
]


def seed_projects(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    for data in PROJECTS:
        Project.objects.get_or_create(slug=data["slug"], defaults=data)


def remove_projects(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    Project.objects.filter(slug__in=[data["slug"] for data in PROJECTS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_projects, remove_projects),
    ]
