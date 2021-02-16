from django.contrib import admin
from django import forms
from django.conf import settings
from django.db import transaction
from .models import User
from lottery.models import Draw, Ticket


class TicketInline(admin.StackedInline):
    model = Ticket
    fields = ("draw",)
    extra = 0

    def get_queryset(self, request):
        current_draw = Draw.objects.current()
        qs = super().get_queryset(request).filter(draw=current_draw)
        return qs


class BalanceChangeForm(admin.helpers.ActionForm):
    amount = forms.IntegerField(min_value=0, max_value=100000)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [TicketInline]

    action_form = BalanceChangeForm
    actions = ["deposit", "withdraw"]

    readonly_fields = [
        "username",
        "first_name",
        "last_name",
        "balance",
        "winnings",
        "telegram_id",
        "phone",
        "extra_tickets_ttl",
    ]
    fields = readonly_fields

    list_display = [
        "username",
        "full_name",
        "telegram_id",
        "balance",
        "winnings",
        "number_of_current_tickets",
        "current_prize",
        "is_staff",
        "is_superuser",
    ]

    list_filter = ["is_staff", "is_superuser", "date_joined"]
    search_fields = ["username", "first_name", "last_name", "alias"]

    def has_add_permission(self, request, obj=None):
        return settings.DEBUG

    def has_delete_permission(self, request, obj=None):
        return False

    @transaction.atomic
    def deposit(self, request, queryset):
        amount = int(request.POST["amount"])
        for user in queryset:
            user.balance += amount
            user.save()

    @transaction.atomic
    def withdraw(self, request, queryset):
        amount = int(request.POST["amount"])
        for user in queryset:
            user.balance -= amount
            user.save()
