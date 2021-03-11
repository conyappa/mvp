from fintoc import Client
from django.conf import settings
from django.db import transaction
from app.utils import Singleton
from .models import Movement


class Fintoc(metaclass=Singleton):
    def __init__(self):
        self.client = Client(api_key=settings.FINTOC_SECRET_KEY)
        self.link = self.client.get_link(link_token=settings.FINTOC_LINK_TOKEN)
        self.account = self.link.find(id_=settings.FINTOC_ACCOUNT_ID)

    def sync(self):
        movements = []
        page = 1

        # Movements are ordered by Fintoc’s post_date.
        latest_movement = Movement.objects.first()
        since = latest_movement and latest_movement.fintoc_post_date

        while True:
            fintoc_movements = self.account.get_transactions(since=since, page=page)
            movements_data = [movement.serialize() for movement in fintoc_movements]
            movements += [Movement(fintoc_data=data) for data in movements_data]
            page += 1

        with transaction.atomic():
            # Ignore duplicated movements (i.e., with the same fintoc_id).
            Movement.objects.bulk_create(movements, ignore_conflicts=True)
