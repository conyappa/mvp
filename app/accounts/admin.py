from admin_numeric_filter.admin import NumericFilterModelAdmin, SliderNumericFilter
from django.contrib import admin
from django import forms
from django.conf import settings
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, CHANGE
from .models import User, EmailListEntry
from lottery.models import Draw, Ticket


class TicketInline(admin.StackedInline):
    model = Ticket
    fields = ("draw",)
    extra = 0

    def get_queryset(self, request):
        current_draw = Draw.objects.current()
        qs = super().get_queryset(request).filter(draw=current_draw)
        return qs


class UserBalanceChangeForm(admin.helpers.ActionForm):
    amount = forms.IntegerField(min_value=0, max_value=100000)


@admin.register(User)
class UserAdmin(NumericFilterModelAdmin):
    inlines = [TicketInline]

    action_form = UserBalanceChangeForm

    actions = [
        "deposit",
        "withdraw",
    ]

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

    other_fields = [
        "alias",
    ]

    fields = other_fields + readonly_fields

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

    list_filter = [
        "is_staff",
        "is_superuser",
        "date_joined",
        ("balance", SliderNumericFilter),
        ("winnings", SliderNumericFilter),
    ]

    search_fields = [
        "username",
        "first_name",
        "last_name",
        "alias",
    ]

    def has_add_permission(self, request):
        return super().has_add_permission(request) and settings.DEBUG

    def has_delete_permission(self, request, obj=None):
        return False

    @transaction.atomic
    def change_balance(self, request, queryset, amount):
        for user in queryset:
            user.balance += amount
            user.save()

            content_type = ContentType.objects.get_for_model(user)

            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=content_type.pk,
                object_id=user.pk,
                object_repr=repr(user),
                action_flag=CHANGE,
                change_message=f"Change Balance ({amount:+})",
            )

    def deposit(self, request, queryset):
        amount = int(request.POST["amount"])
        self.change_balance(request, queryset, amount)

    def withdraw(self, request, queryset):
        amount = int(request.POST["amount"])
        amount *= -1
        self.change_balance(request, queryset, amount)


@admin.register(EmailListEntry)
class EmailListEntryAdmin(NumericFilterModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj) and settings.DEBUG
