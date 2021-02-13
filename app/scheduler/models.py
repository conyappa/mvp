from django.db import models
from app.base import BaseModel


class ScheduledMessage(BaseModel):
    class Meta:
        ordering = ("scheduled_for",)

    scheduled_for = models.DateTimeField(verbose_name="scheduled for")
    text = models.TextField(verbose_name="message text")
    draft = models.BooleanField(default=False, verbose_name="draft status")
    sent = models.BooleanField(default=False, verbose_name="sent status")
