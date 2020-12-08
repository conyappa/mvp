from django.conf import settings
from .main import get_scheduler


def use_scheduler(task):
    def wrapper(*args, **kwargs):
        scheduler = get_scheduler()
        task(*args, **kwargs, scheduler=scheduler)

    return wrapper


@use_scheduler
def add_draw_creation_job(draw_model, scheduler):
    draw_creation_day_of_week = (settings.DRAW_BEGINNING_DAY_OF_WEEK - settings.DRAW_CREATION_DAYS_DELTA) % 7
    scheduler.add_job(
        draw_model.objects.create,
        "cron",
        day_of_week=draw_creation_day_of_week,
        hour=settings.DRAW_RESULTS_HOUR,
    )


@use_scheduler
def add_result_choice_job(draw, scheduler):
    for days_delta in range(0, 7):
        run_date = draw.start_date + dt.timedelta(days=days_delta, hours=settings.DRAW_RESULTS_HOUR)
        scheduler.add_job(draw.choose_results, "date", run_date=run_date, kwargs={"k": 1})
