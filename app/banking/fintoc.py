from logging import getLogger
from fintoc import Client
from django.conf import settings
from django.db import transaction, IntegrityError
from app.utils import Singleton
from .models import Movement


logger = getLogger(__name__)


class Fintoc(metaclass=Singleton):
    def __init__(self):
        self.client = Client(api_key=settings.FINTOC_SECRET_KEY)
        self.link = self.client.get_link(link_token=settings.FINTOC_LINK_TOKEN)
        self.account = self.link.find(id_=settings.FINTOC_ACCOUNT_ID)

    @transaction.atomic
    def fetch(self):
        query_params = {"page": 1}

        # Movements are ordered by Fintoc’s post_date.
        latest_movement = Movement.objects.first()

        if latest_movement is not None:
            query_params["since"] = latest_movement.fintoc_post_date

        while True:
            fintoc_movements = list(self.account.get_movements(**query_params))

            if not fintoc_movements:
                break

            for obj in fintoc_movements:
                data = obj.serialize()

                try:
                    fintoc_id = data.get("id")
                    fintoc_post_datetime = data.get("post_date")
                    fintoc_post_date = fintoc_post_datetime.split("T")[0]

                    # Use regular create instead of bulk_create so the post_save signal is sent.
                    Movement.objects.create(fintoc_data=data, fintoc_id=fintoc_id, fintoc_post_date=fintoc_post_date)

                except IntegrityError:
                    # Ignore duplicated movements (i.e., with the same fintoc_id).
                    pass

            query_params["page"] += 1
