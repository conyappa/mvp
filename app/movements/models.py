from django.db import models
from app.base import BaseModel


class Movement(BaseModel):
    user = models.ForeignKey(
        to="account.User",
        null=True,
        default=None,
        verbose_name="user",
        related_name="movements",
        on_delete=models.PROTECT,
    )
    fintoc_data = models.JSONField(verbose_name="Fintoc movement object")

    def __init__(self, fintoc_data):
        super()

    @property
    def amount(self):
        return self.fintoc_data.get("amount")

    @property
    def rut(self):
        sender_account = self.fintoc_data.get("sender_account", {})
        return sender_account.get("holder_id")
