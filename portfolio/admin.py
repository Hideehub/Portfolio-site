from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "order", "is_featured", "live_url", "created_at"]
    list_editable = ["order", "is_featured"]
    list_filter = ["is_featured"]
    search_fields = ["title", "summary", "tech_stack"]
    prepopulated_fields = {"slug": ["title"]}
