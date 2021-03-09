from django.db import models
from app.base import BaseModel


class Movement(BaseModel):
    fintoc_data = models.JSONField(verbose_name="Fintoc movement object")

    user = models.ForeignKey(
        to="accounts.User",
        null=True,
        default=None,
        verbose_name="user",
        related_name="movements",
        on_delete=models.PROTECT,
    )

    @property
    def amount(self):
        return self.fintoc_data.get("amount")

    @property
    def raw_rut(self):
        sender_account = self.fintoc_data.get("sender_account", {})
        return sender_account.get("holder_id")

    @property
    def rut(self):
        raw_rut = self.raw_rut
        return int(raw_rut[:-1]) if isinstance(raw_rut, str) else None
