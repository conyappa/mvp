import threading
from apscheduler.schedulers.background import BackgroundScheduler


_scheduler = threading.local()


def boot_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.start()
    _scheduler.value = scheduler


def get_scheduler():
    return _scheduler.value
