import logging
from django.db.models import signals
from django.dispatch import receiver
from .models import Message


logger = logging.getLogger(__name__)


@receiver(signal=signals.post_save, sender=Message)
def message_update_scheduler(sender, instance, created, update_fields, *args, **kwargs):
    if update_fields and ("job_id" in update_fields):
        return

    if instance.is_ready:
        if instance.has_job:
            instance.reschedule_job()
        else:
            instance.schedule_job()

    elif instance.has_job:
        instance.remove_job()


@receiver(signal=signals.pre_delete, sender=Message)
def message_remove_job(sender, instance, *args, **kwargs):
    if instance.has_job:
        instance.remove_job()
