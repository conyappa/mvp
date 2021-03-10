from django.db import models
from app.base import BaseModel


class Movement(BaseModel):
    class Meta:
        ordering = ["-fintoc_post_date"]
        indexes = [models.Index(fields=["fintoc_id"])]

    fintoc_data = models.JSONField(verbose_name="Fintoc movement object")
    fintoc_id = models.CharField(unique=True, verbose_name="Fintoc movement 'id'", max_length=32)
    fintoc_post_date = models.DateField(verbose_name="Fintoc movement 'post_date'")

    user = models.ForeignKey(
        to="accounts.User",
        null=True,
        default=None,
        verbose_name="user",
        related_name="movements",
        on_delete=models.PROTECT,
    )

    def __init__(self, **kwargs):
        fintoc_data = kwargs.pop("fintoc_data", {})
        fintoc_id = fintoc_data.get("id")
        fintoc_post_date = fintoc_data.get("post_date")

        super().__init__(fintoc_data=fintoc_data, fintoc_id=fintoc_id, fintoc_post_date=fintoc_post_date, **kwargs)

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
