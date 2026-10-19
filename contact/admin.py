from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "created_at", "is_read"]
    list_editable = ["is_read"]
    list_filter = ["is_read", "created_at"]
    search_fields = ["name", "email", "message"]
    readonly_fields = ["name", "email", "message", "created_at"]
    actions = ["mark_as_read"]

    def has_add_permission(self, request):
        return False

    @admin.action(description="Mark selected messages as read")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
