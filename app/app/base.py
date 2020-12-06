import uuid
from django.db import models
from django.utils import timezone


class BaseManagerMixin:
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class BaseModelManager(BaseManagerMixin, models.Manager):
    pass


class BaseModelMixin:
    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        serialize=False,
        unique=True,
        verbose_name="identifier",
    )

    is_active = models.BooleanField(
        default=True,
        help_text=(
            "Designates whether this object should be treated as active. "
            "Unselect this instead of deleting it."
        ),
        verbose_name="active status",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="last updated at")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="last deleted at")

    objects = managers.BaseModelManager()

    def save(self, *args, **kwargs):
        self.clean_fields()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save(*args, **kwargs)

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
