import threading
from apscheduler.schedulers.background import BackgroundScheduler


_scheduler = threading.local()


def boot_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.start()
    _scheduler.value = scheduler


def use_scheduler(task):
    return lambda *args, **kwargs: task(*args, **kwargs, scheduler=_scheduler.value)
