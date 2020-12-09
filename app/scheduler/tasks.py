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
    if now.weekday() == settings.DRAW_BEGINNING_DAY_OF_WEEK:
        draw = Draw.objects.create(start_date=now.date())
        draw.create_tickets()
    if Draw.objects.exists():
        draw = Draw.objects.current()
        draw.choose_result()


@use_scheduler
def add_draw_cycle_job(scheduler):
    scheduler.add_job(draw_cycle, "cron", hour=settings.DRAW_RESULTS_HOUR)