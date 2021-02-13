from django.contrib import admin
from .models import ScheduledMessage


@admin.register(ScheduledMessage)
class ScheduledMessageAdmin(admin.ModelAdmin):
    readonly_fields = ("sent",)
    list_display = ("scheduled_for", "text", "is_draft", "sent")
    list_filter = ("scheduled_for", "is_draft", "sent")
    search_fields = ("text",)

    def has_change_permission(self, request, obj=None):
        return obj and (not obj.sent)

    def has_delete_permission(self, request, obj=None):
        return obj and (not obj.sent)
