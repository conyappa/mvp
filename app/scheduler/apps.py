from logging import getLogger
from django.apps import AppConfig
from django.conf import settings


logger = getLogger(__name__)


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

        if settings.FINTOC_IS_ENABLED:
            tasks.add_fintoc_movements_fetcher()

        try:
            Message.objects.schedule_jobs()
        except Exception as e:
            logger.warning(f"Unable to schedule messages: {e}")
        else:
            logger.info("Successfully scheduled all messages.")
