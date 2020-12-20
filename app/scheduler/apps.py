from django.apps import AppConfig


class SchedulerConfig(AppConfig):
    name = "scheduler"

    def ready(self):
        from .helpers import boot_scheduler
        from .tasks import add_draw_cycle_job

        boot_scheduler()
        add_draw_cycle_job()
