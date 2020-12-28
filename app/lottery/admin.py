from django.contrib import admin
from .models import Draw, Ticket


class LotteryAdminMixin:
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Draw)
class DrawAdmin(LotteryAdminMixin, admin.ModelAdmin):
    readonly_fields = ("start_date", "pool", "results")
    list_filter = ("start_date",)


@admin.register(Ticket)
class TicketAdmin(LotteryAdminMixin, admin.ModelAdmin):
    readonly_fields = ("picks", "draw", "user")
    list_filter = ("draw", "user")
    search_fields = ("user__username", "user__first_name", "user__last_name")
