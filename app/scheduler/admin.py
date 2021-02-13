import logging
from django import forms
from django.contrib import admin
from .models import Message


logger = logging.getLogger(__name__)


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


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    form = MessageForm
    list_display = ("scheduled_for", "preview", "status", "job_id")
    list_filter = ("scheduled_for", "status")
    search_fields = ("text",)

    def has_change_permission(self, request, obj=None):
        return obj and (obj.status != Message.Status.SENT)

    def has_delete_permission(self, request, obj=None):
        return obj and (obj.status != Message.Status.SENT)

    def preview(self, obj):
        max_lenght = 100
        suffix = "…" if (len(obj.text) > max_lenght) else ""
        return obj.text[:max_lenght] + suffix
