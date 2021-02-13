import datetime as dt
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from bot.sender import MultiSender
from accounts.models import User
from app.base import BaseModel
from .helpers import use_scheduler


def validate_scheduled_too_soon(value):
    now = timezone.localtime()
    in_one_minute = now + dt.timedelta(minutes=1)
    if value <= in_one_minute:
        raise ValidationError("The scheduled time is too soon.")


class MessageManager(models.Manager):
    def schedule(self):
        for message in self.filter(scheduled_for__isnull=False, is_draft=False, sent=False):
            message.schedule()


class Message(BaseModel):
    class Meta:
        ordering = ("scheduled_for",)

    scheduled_for = models.DateTimeField(
        blank=True, null=True, validators=[validate_scheduled_too_soon], verbose_name="scheduled for"
    )
    job_id = models.CharField(null=True, max_length=64, default=None, verbose_name="scheduler job ID")

    text = models.TextField(verbose_name="message text")

    is_draft = models.BooleanField(default=False, verbose_name="draft status")
    sent = models.BooleanField(default=False, verbose_name="sent status")

    objects = MessageManager()

    @use_scheduler
    def schedule_job(self, scheduler):
        job = scheduler.add_job(self.send, args=(self,), trigger="date", run_date=self.scheduled_for)
        self.job_id = job.id
        self.save()

    @use_scheduler
    def reschedule_job(self, scheduler):
        scheduler.reschedule_job(self.job_id, trigger="date", run_date=self.scheduled_for)

    @use_scheduler
    def remove_job(self, scheduler):
        scheduler.remove_job(self.job_id)
        self.job_id = None
        self.save()

    def send(self):
        MultiSender().send_async(
            users=User.objects.all(), msg_body_formatter=lambda _user: self.text, interfaces=("telegram",)
        )
        self.sent = True
        self.save()

    @property
    def is_ready(self):
        return (self.scheduled_for is not None) and (not self.is_draft)

    @property
    def has_job(self):
        return self.job_id is not None
