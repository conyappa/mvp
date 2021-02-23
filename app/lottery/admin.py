from django.contrib import admin
from django.conf import settings
from .models import Draw, Ticket


@admin.register(Draw)
class DrawAdmin(admin.ModelAdmin):
    readonly_fields = [
        "start_date",
        "pool",
        "results",
    ]

    list_display = [
        "start_date",
        "results",
        "pool",
    ]

    list_filter = [
        "start_date",
    ]

    def has_add_permission(self, request):
        return super().has_add_permission(request) and settings.DEBUG

    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj) and settings.DEBUG

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj) and settings.DEBUG


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    readonly_fields = [
        "picks",
        "draw",
        "user",
    ]

    list_display = [
        "user",
        "draw",
        "picks",
    ]

    list_filter = [
        "draw",
    ]

    search_fields = [
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__alias",
    ]

    def has_add_permission(self, request):
        return super().has_add_permission(request) and settings.DEBUG

    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj) and settings.DEBUG

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj) and settings.DEBUG
