from django.db.models import signals
from django.dispatch import receiver
from .models import User
from lottery.models import Draw


@receiver(signal=signals.post_save, sender=User)
def user_join_current_draw(sender, instance, created, *args, **kwargs):
    if created:
        if Draw.objects.exists():
            Draw.objects.current().include_new_user(user=instance)
