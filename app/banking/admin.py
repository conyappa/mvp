from django.contrib import admin
from django.conf import settings
from .models import Movement


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    readonly_fields = [
        "fintoc_data",
        "fintoc_post_date",
        "number",
        "amount",
    ]

    other_fields = [
        "user",
    ]

    fields = other_fields + readonly_fields

    list_display = [
        "user",
        "amount",
        "fintoc_post_date",
    ]

    list_filter = ["user", "fintoc_post_date"]

    search_fields = [
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__alias",
    ]

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj) and settings.DEBUG
