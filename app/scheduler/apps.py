from django.apps import AppConfig


class SchedulerConfig(AppConfig):
    name = "scheduler"

    def ready(self):
        from .helpers import boot_scheduler
        from . import tasks
        from .models import ScheduledMessage

        boot_scheduler()

        tasks.add_new_draw_reminder_cycle()
        tasks.add_new_draw_creation_cycle()
        tasks.add_ongoing_draw_cycle()

        ScheduledMessage.objects.anticipated().schedule()
