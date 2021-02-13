from django.contrib import admin
from .models import ScheduledMessage


@admin.register(ScheduledMessage)
class DrawAdmin(admin.ModelAdmin):
    readonly_fields = ("sent",)
    list_display = ("scheduled_for", "text", "is_draft", "sent")
    list_filter = ("scheduled_for", "is_draft", "sent")
    search_fields = ("text",)
