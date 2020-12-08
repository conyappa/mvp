from django.apps import AppConfig


class LotteryConfig(AppConfig):
    name = "lottery"

    def ready(self):
        from scheduler.tasks import add_draw_creation_job
        from .models import Draw

        add_draw_creation_job(Draw)
