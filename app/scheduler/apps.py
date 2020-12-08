from django.apps import AppConfig


class SchedulerConfig(AppConfig):
    name = "scheduler"

    def ready(self):
        from lottery.models import Draw
        from .main import boot_scheduler
        from .tasks import add_draw_creation_job

        boot_scheduler()
        add_draw_creation_job(Draw)
