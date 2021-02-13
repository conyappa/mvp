from django.db.models import signals
from django.dispatch import receiver
from .models import Message


@receiver(signal=signals.post_save, sender=Message)
def message_schedule(sender, instance, created, *args, **kwargs):
    if instance.is_ready:
        if created:
            instance.schedule()
        elif instance:
            instance.reschedule()


@receiver(signal=signals.pre_delete, sender=Message)
def message_remove(sender, instance, *args, **kwargs):
    if instance.has_job:
        instance.remove_job()
