from logging import getLogger
import datetime as dt
from django import forms
from django.contrib import admin
from django.utils import timezone
from django.db.models import Q
from .models import Message


logger = getLogger(__name__)


class MessageForm(forms.ModelForm):
    class Meta:
        fields = ("scheduled_for", "text")
        model = Message

    draft = forms.BooleanField(required=False, initial=False, label="Draft")

    def save(self, commit=True):
        draft = self.cleaned_data.pop("draft", False)

        status = Message.Status.DRAFT if draft else Message.Status.SCHEDULED
        self.instance.status = status

        return super().save(commit=commit)


class MessageStatusFieldListFilter(admin.SimpleListFilter):
    title = "status"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return (
            ("relevant", "Relevant"),
            ("not sent", "Not sent"),
            ("sent", "Sent"),
        )

    def queryset(self, request, queryset):
        value = self.value()
        qs = queryset

        if value == "relevant":
            now = timezone.localtime()
            yesterday = now - dt.timedelta(days=1)
            query = Q(scheduled_for__gte=yesterday) | (~Q(status=Message.Status.SENT))
            qs = qs.filter(query)

        elif value == "not sent":
            qs = qs.exclude(status=Message.Status.SENT)

        elif value == "sent":
            qs = qs.filter(status=Message.Status.SENT)

        return qs


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    form = MessageForm

    list_display = ["scheduled_for", "preview", "status", "job_id"]

    list_filter = ["scheduled_for", MessageStatusFieldListFilter]
    search_fields = ["text"]

    def has_change_permission(self, request, obj=None):
        return obj and (obj.status != Message.Status.SENT)

    def has_delete_permission(self, request, obj=None):
        return obj and (obj.status != Message.Status.SENT)

    def preview(self, obj):
        max_lenght = 100
        suffix = "…" if (len(obj.text) > max_lenght) else ""
        return obj.text[:max_lenght] + suffix
