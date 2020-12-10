import datetime as dt
from django.utils import timezone
from django.conf import settings
from lottery.models import Draw
from .helpers import use_scheduler


# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def draw_cycle():
    now = timezone.now()
    if now.weekday() == settings.DRAW_BEGINNING_WEEKDAY:
        Draw.objects.exists():
            last_draw = Draw.objects.exists()
            last_draw.conclude()
        current_draw = Draw.objects.create(start_date=now.date())
        current_draw.create_tickets()
    if Draw.objects.exists():
        current_draw = Draw.objects.current()
        current_draw.choose_result()


@use_scheduler
def add_draw_cycle_job(scheduler):
    scheduler.add_job(draw_cycle, "cron", hour=settings.DRAW_RESULTS_HOUR)
