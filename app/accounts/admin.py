from django.contrib import admin
from .models import User
from lottery.models import Draw, Ticket


class AccountsAdminMixin:
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class TicketInline(admin.StackedInline):
    model = Ticket
    fields = ("draw",)
    extra = 0

    def get_queryset(self, request):
        current_draw = Draw.objects.current()
        queryset = super().get_queryset(request).filter(draw=current_draw)
        return queryset


@admin.register(User)
class UserAdmin(AccountsAdminMixin, admin.ModelAdmin):
    inlines = (TicketInline,)
    readonly_fields = (
        "username",
        "password",
        "first_name",
        "last_name",
        "last_login",
        "date_joined",
        "telegram_id",
        "phone",
        "winnings",
        "extra_tickets_ttl",
    )
    list_display = (
        "username",
        "full_name",
        "alias",
        "telegram_id",
        "balance",
        "winnings",
        "number_of_current_tickets",
        "current_prize",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("is_staff", "is_superuser", "date_joined")
    search_fields = ("username", "first_name", "last_name", "alias")
