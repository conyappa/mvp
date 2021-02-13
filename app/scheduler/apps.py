import logging
from django.apps import AppConfig


logger = logging.getLogger(__name__)


class SchedulerConfig(AppConfig):
    name = "scheduler"

    def ready(self):
        from .helpers import boot_scheduler
        from . import tasks
        from .models import Message
        from . import signals  # noqa: F401

        boot_scheduler()

        tasks.add_new_draw_reminder_cycle()
        tasks.add_new_draw_creation_cycle()
        tasks.add_ongoing_draw_cycle()

        try:
            Message.objects.schedule_jobs()
        except Exception as e:
            logger.warning(f"Unable to schedule messages: {e}")
        else:
            logger.info("Successfully scheduled all messages.")
