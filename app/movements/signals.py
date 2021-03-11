from logging import getLogger
from django.db.models import signals
from django.dispatch import receiver
from django.db import transaction
from accounts.models import User
from .models import Movement


logger = getLogger(__name__)


@receiver(signal=signals.post_save, sender=Movement)
def associate_movement_w_user(sender, instance, created, *args, **kwargs):
    if created:
        movement_rut = instance.rut

        try:
            user = User.objects.get(rut=movement_rut)
        except User.DoesNotExist as e:
            logger.warning(f"Couldn’t associate movement to user: {e}")
        else:
            with transaction.atomic():
                instance.set_user(user=user)
                instance.save()

                user.balance += instance.amount
                user.save()
