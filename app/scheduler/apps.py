from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler


class SchedulerConfig(AppConfig):
    name = "scheduler"

    def ready(self):
        from lottery.models import Draw

        scheduler = BackgroundScheduler()
        scheduler.start()
        Draw.attach_creation_schedule(scheduler)
