from django.db.models import signals
from django.dispatch import receiver
from .models import ScheduledMessage


@receiver(signal=signals.post_save, sender=ScheduledMessage)
def message_schedule(sender, instance, created, *args, **kwargs):
    if instance.is_ready:
        if created:
            instance.schedule()
        elif instance:
            instance.reschedule()


@receiver(signal=signals.pre_delete, sender=ScheduledMessage)
def message_remove(sender, instance, *args, **kwargs):
    if instance.has_job:
        instance.remove_job()
