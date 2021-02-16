from logging import getLogger
import datetime as dt
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from bot.telegram.sender import Client
from accounts.models import User
from app.base import BaseModel
from .helpers import use_scheduler


logger = getLogger(__name__)


def validate_scheduled_time(value):
    now = timezone.localtime()
    in_one_minute = now + dt.timedelta(minutes=1)

    if value < now:
        raise ValidationError("The scheduled time already passed.")
    if value <= in_one_minute:
        raise ValidationError("The scheduled time is too soon.")


class MessageManager(models.Manager):
    def schedule_jobs(self):
        for message in self.filter(scheduled_for__isnull=False, status=Message.Status.SCHEDULED):
            message.schedule_job()


class Message(BaseModel):
    class Meta:
        ordering = ("scheduled_for",)

    class Status(models.IntegerChoices):
        DRAFT = 1
        SCHEDULED = 2
        SENT = 3

    text = models.TextField(verbose_name="text")

    scheduled_for = models.DateTimeField(
        blank=True, null=True, validators=[validate_scheduled_time], verbose_name="scheduled for"
    )
    job_id = models.CharField(null=True, max_length=64, default=None, verbose_name="scheduler job ID")
    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.SCHEDULED, verbose_name="status")

    objects = MessageManager()

    @use_scheduler
    def schedule_job(self, scheduler):
        job = scheduler.add_job(self.send, trigger="date", run_date=self.scheduled_for)
        self.job_id = job.id
        # Add this update_fields argument for the post_save signal.
        self.save(update_fields={"job_id"})

    @use_scheduler
    def reschedule_job(self, scheduler):
        scheduler.reschedule_job(self.job_id, trigger="date", run_date=self.scheduled_for)

    @use_scheduler
    def remove_job(self, scheduler):
        scheduler.remove_job(self.job_id)
        self.job_id = None
        # Add this update_fields argument for the post_save signal.
        self.save(update_fields={"job_id"})

    def send(self):
        Client().send_async(msg_formatter=lambda _user: self.text, users=User.objects.all())
        self.status = Message.Status.SENT
        self.save()

    @property
    def is_ready(self):
        return (self.scheduled_for is not None) and (self.status == Message.Status.SCHEDULED)

    @property
    @use_scheduler
    def has_job(self, scheduler):
        return bool(self.job_id and scheduler.get_job(self.job_id))
