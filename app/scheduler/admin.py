import datetime as dt
from django.contrib import admin
from django.db.models import Q
from django.utils import timezone
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

    def get_queryset(self, request):
        now = timezone.localtime()
        yesterday = now - dt.timedelta(days=1)
        query = Q(sent=False) | Q(scheduled_for__gte=yesterday)
        qs = super().get_queryset(request).filter(query)
        return qs
