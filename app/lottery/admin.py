from django.contrib import admin
from .models import Draw, Ticket


class LotteryAdminMixin:
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(Draw)
class DrawAdmin(LotteryAdminMixin, admin.ModelAdmin):
    readonly_fields = ("start_date", "pool", "results")
    list_display = ("start_date", "results", "pool")
    list_filter = ("start_date",)


@admin.register(Ticket)
class TicketAdmin(LotteryAdminMixin, admin.ModelAdmin):
    readonly_fields = ("picks", "draw", "user")
    list_display = ("user", "draw", "picks")
    list_filter = ("draw", "user")
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__alias")
